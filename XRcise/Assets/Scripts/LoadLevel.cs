using UnityEngine;
using UnityEngine.SceneManagement;

public class LoadLevel : MonoBehaviour
{
    public string levelname;

    public void loadlevel()
    {
        SceneManager.LoadScene(levelname);
    }
}
