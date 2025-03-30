using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using System.Collections;
using System.Text;
using System.Collections.Generic;
using UnityEngine.EventSystems;

public class APIRequest : MonoBehaviour
{
    public GameObject[] Buttons1;
    public GameObject[] Buttons2;
    public GameObject[] Buttons3;
    public GameObject[] Buttons4;

    public TMP_Text Header;

    public GameObject OutputPanel;
    
    public TMP_Text recommendedExerciseText;
    public TMP_Text frequencyText;

    private Dictionary<string, string> selectedValues = new Dictionary<string, string>(); // Stores user selections


    private string[] apiUrl; // Change this if needed

    public void Start()
    {
        apiUrl = new string[] { "http://192.168.137.227:8000/predict", "http://127.10.20.11:8000/predict", "http://192.168.137.227:8000/predict", "http://192.168.137.227:8000/predict" };

        foreach (GameObject btn in Buttons1)
        {
            btn.SetActive(true);
        }
        foreach (GameObject btn in Buttons2)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons3)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons4)
        {
            btn.SetActive(false);
        }
    }

    public void GetButtonClick1()
    {
        GameObject clickedButton = EventSystem.current.currentSelectedGameObject; // Get clicked button
        selectedValues["1"] = clickedButton.name;
        Debug.Log(clickedButton.name);
        Header.text = "What is your Age?";
        foreach (GameObject btn in Buttons2)
        {
            btn.SetActive(true);
        }
        foreach (GameObject btn in Buttons1)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons3)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons4)
        {
            btn.SetActive(false);
        }
    }

    public void GetButtonClick2()
    {
        GameObject clickedButton = EventSystem.current.currentSelectedGameObject; // Get clicked button
        selectedValues["2"] = clickedButton.name;
        Debug.Log(clickedButton.name);
        Header.text = "What is your Pain Intensity?";

        foreach (GameObject btn in Buttons3)
        {
            btn.SetActive(true);
        }
        foreach (GameObject btn in Buttons2)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons1)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons4)
        {
            btn.SetActive(false);
        }
    }

    public void GetButtonClick3()
    {
        GameObject clickedButton = EventSystem.current.currentSelectedGameObject; // Get clicked button
        selectedValues["3"] = clickedButton.name;
        Debug.Log(clickedButton.name);
        Header.text = "What is your Exercise Capicity?";

        foreach (GameObject btn in Buttons4)
        {
            btn.SetActive(true);
        }
        foreach (GameObject btn in Buttons3)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons2)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons1)
        {
            btn.SetActive(false);
        }
    }

    public void GetButtonClick4()
    {
        GameObject clickedButton = EventSystem.current.currentSelectedGameObject; // Get clicked button
        selectedValues["4"] = clickedButton.name;
        Debug.Log(clickedButton.name);
        SendRequest();
        foreach (GameObject btn in Buttons4)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons3)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons2)
        {
            btn.SetActive(false);
        }
        foreach (GameObject btn in Buttons1)
        {
            btn.SetActive(false);
        }
    }

    public void SendRequest()
    {
        // ✅ Construct JSON string manually
        string jsonString = "{ \"responses\": { " +
            "\"pain_location\": \"" + selectedValues["1"] + "\", " +
            "\"age_group\": \"" + selectedValues["2"] + "\", " +
            "\"pain_intensity\": \"" + selectedValues["3"] + "\", " +
            "\"physical_capicity\": \"" + selectedValues["4"] + "\" " +
            "} }";

        Debug.Log("Final JSON Payload: " + jsonString);
            
        foreach(string apiend in apiUrl)
        {
            // ✅ Send API Request
            StartCoroutine(PostRequest(apiend, jsonString));
        }
    }


IEnumerator PostRequest(string url, string json)
{
    using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
    {
        byte[] bodyRaw = Encoding.UTF8.GetBytes(json);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        Debug.Log("Sending API request...");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            string responseText = request.downloadHandler.text;
            Debug.Log("✅ API Response: " + responseText);
            OutputPanel.SetActive(true);

            // ✅ Parse JSON Response
            var jsonResponse = JsonUtility.FromJson<APIResponse>(responseText);

            // ✅ Use StringBuilder for setting TMP text
            StringBuilder sb = new StringBuilder();
            sb.Append(" ");
            sb.Append(jsonResponse.recommended_exercise);

            recommendedExerciseText.text = sb.ToString();

            sb.Clear();
            sb.Append(" ");
            sb.Append(jsonResponse.frequency);

            frequencyText.text = sb.ToString();
        }
        else
        {
            Debug.LogError($"❌ Request Failed: {request.responseCode} - {request.error}");
            Debug.LogError("Response Body: " + request.downloadHandler.text);
        }
    }
}

// ✅ Helper class for JSON Parsing
[System.Serializable]
public class APIResponse
{
    public int prediction;
    public string recommended_exercise;
    public string frequency;
}

}
