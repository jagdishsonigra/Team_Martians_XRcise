using UnityEngine;

public class ForearmSwing : MonoBehaviour
{
    private Transform forearmR;
    public float speed = 1.5f;
    private float minRotation = -168f;
    private float maxRotation = -41.51f;
    private bool movingUp = true;

    void Start()
    {
        // Find the forearm.R bone dynamically
        forearmR = FindDeepChild(transform, "forearm.R");

        if (!forearmR)
        {
            Debug.LogError("forearm.R not found! Check bone names.");
        }
    }

    void Update()
    {
        if (!forearmR) return;

        float targetZ = movingUp ? maxRotation : minRotation;
        Quaternion targetRotation = Quaternion.Euler(forearmR.localEulerAngles.x, forearmR.localEulerAngles.y, targetZ);
        forearmR.localRotation = Quaternion.RotateTowards(forearmR.localRotation, targetRotation, speed * Time.deltaTime * 100);

        if (Quaternion.Angle(forearmR.localRotation, targetRotation) < 1f)
        {
            movingUp = !movingUp;
        }
    }

    // Helper function to find bones dynamically
    Transform FindDeepChild(Transform parent, string name)
    {
        foreach (Transform child in parent)
        {
            if (child.name == name)
                return child;

            Transform found = FindDeepChild(child, name);
            if (found != null)
                return found;
        }
        return null;
    }
}