using UnityEngine;
using TMPro; // Import for TextMeshPro

public class PlayerController : MonoBehaviour
{
    public int lives = 3; // Player starts with 3 lives
    public TMP_Text livesText; // Assign the TextMeshPro UI in Inspector
    public SquatController gameController; // Reference to SquatController script

    private void Start()
    {
        UpdateLivesText();
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("disco")) // If collided with projectile
        {
            lives--; // Decrement lives
            UpdateLivesText();
            Destroy(other.gameObject); // Destroy the projectile

            if (lives <= 0)
            {
                gameController.StopGame(); // Stop game when lives reach 0
            }
        }
    }

    private void UpdateLivesText()
    {
        livesText.text = "Lives: " + lives;
    }
}
