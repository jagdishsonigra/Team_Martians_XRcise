using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine.UI;
using TMPro; // Import TextMeshPro namespace

public class SocketClient : MonoBehaviour
{
    private TcpClient client;
    private NetworkStream stream;
    private Thread receiveThread;
    private string receivedData = "Waiting...";
    private int exerciseCount = 0;
    private float percentage = 0f;

    public string exerciseName = "Arm Movement"; // Public string for exercise name
    public TMP_Text countText; // TMP Text for exercise count
    public Slider percentageSlider; // UI Slider to display percentage
    public GameObject redLight; // Red light GameObject
    public GameObject greenLight; // Green light GameObject

    private string serverIP = "172.20.10.2";

    void OnEnable()
    {
        ConnectToServer();
    }
    
    void ConnectToServer()
    {
        try
        {
            client = new TcpClient(serverIP, 5005); // Replace with your PC's local IP
            stream = client.GetStream();

            // Send the exercise name to the server
            byte[] data = Encoding.UTF8.GetBytes(exerciseName);
            stream.Write(data, 0, data.Length);
            Debug.Log("Sent exercise: " + exerciseName);

            // Start receiving data in a separate thread
            receiveThread = new Thread(new ThreadStart(ReceiveData));
            receiveThread.IsBackground = true;
            receiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.LogError("Connection error: " + e.Message);
        }
    }

    void ReceiveData()
    {
        byte[] buffer = new byte[1024];
        while (client != null && client.Connected)
        {
            try
            {
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead > 0)
                {
                    string message = Encoding.UTF8.GetString(buffer, 0, bytesRead).Trim();
                    receivedData = message;
                    Debug.Log("Received: " + receivedData);

                    // Parse the received data
                    string[] metrics = receivedData.Split(',');
                    if (metrics.Length == 4)
                    {
                        float angle = float.Parse(metrics[0]);
                        float per = float.Parse(metrics[1]);
                        float bar = float.Parse(metrics[2]);
                        exerciseCount = int.Parse(metrics[3]);

                        // Update UI elements in Unity main thread
                        percentage = per;
                    }
                }
            }
            catch (Exception e)
            {
                Debug.LogError("Receive error: " + e.Message);
                break;
            }
        }
    }

    void Update()
    {
        // Update the slider value
        percentageSlider.value = percentage;

        // Update exercise count TMP text
        countText.text = "Count: " + exerciseCount;

        // Toggle lights based on percentage threshold
        if (percentage > 50)
        {
            greenLight.SetActive(true);
            redLight.SetActive(false);
        }
        else
        {
            greenLight.SetActive(false);
            redLight.SetActive(true);
        }
    }

    void OnDisable()
    {
        DisconnectFromServer();
    }

    void DisconnectFromServer()
    {
        if (receiveThread != null && receiveThread.IsAlive)
        {
            receiveThread.Abort();
        }
        if (stream != null)
        {
            stream.Close();
        }
        if (client != null)
        {
            client.Close();
        }
        Debug.Log("Disconnected from server.");
    }
}
