using UnityEngine;
using UnityEngine.UI;

public class ExerciseController : MonoBehaviour
{
    public GameObject idleAnimation; // Assign the Idle animation GameObject
    public GameObject[] exercises;   // Assign all exercise animation GameObjects
    public Button[] exerciseButtons; // Assign all buttons controlling the exercises

    void Start()
    {
        // Ensure only the idle animation is active at start
        SetActiveExercise(idleAnimation);

        // Assign button click events dynamically
        for (int i = 0; i < exerciseButtons.Length; i++)
        {
            int index = i; // Capture correct index
            exerciseButtons[i].onClick.AddListener(() => SetActiveExercise(exercises[index]));
        }
    }

    // Function to activate the selected exercise and deactivate others
    void SetActiveExercise(GameObject activeExercise)
    {
        // Disable all exercises
        foreach (GameObject exercise in exercises)
        {
            exercise.SetActive(false);
        }

        // Disable Idle animation if another exercise is selected
        idleAnimation.SetActive(activeExercise == idleAnimation);

        // Activate selected exercise
        activeExercise.SetActive(true);
    }
}
