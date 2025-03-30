using UnityEngine;
using TMPro;

public class backbutton : MonoBehaviour
{
    public GameObject outputscreen;
    public TMP_Text Header;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public GameObject[] Buttons1;

    public void backbuttonpress()
    {
        Header.text = "What is your Pain Location?";
        foreach (GameObject btn in Buttons1)
        {
            btn.SetActive(true);
        }
        outputscreen.SetActive(false);
    }
}
