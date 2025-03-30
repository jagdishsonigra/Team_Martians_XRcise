using System.Collections;
using UnityEngine;

public class SquatController : MonoBehaviour
{
    public GameObject projectilePrefab;
    public Transform spawnPoint;
    public float spawnInterval = 4f;
    public float moveSpeed = 2f;
    private Coroutine spawnCoroutine;

    public void StartGame()
    {
        spawnCoroutine = StartCoroutine(SpawnProjectiles());
    }

    public void StopGame()
    {
        if (spawnCoroutine != null)
        {
            StopCoroutine(spawnCoroutine);
        }
        DestroyAllProjectiles();
    }

    IEnumerator SpawnProjectiles()
    {
        while (true)
        {
            GameObject projectile = Instantiate(projectilePrefab, new Vector3(24f, spawnPoint.position.y, spawnPoint.position.z), Quaternion.identity);
            projectile.tag = "disco"; // Ensure projectiles are tagged correctly
            StartCoroutine(MoveProjectile(projectile));
            yield return new WaitForSeconds(spawnInterval);
        }
    }

    IEnumerator MoveProjectile(GameObject projectile)
    {
        while (projectile != null && projectile.transform.position.x > 0f)
        {
            projectile.transform.position -= new Vector3(moveSpeed * Time.deltaTime, 0, 0);
            yield return null;
        }
        if (projectile != null)
        {
            Destroy(projectile);
        }
    }

    private void DestroyAllProjectiles()
    {
        GameObject[] projectiles = GameObject.FindGameObjectsWithTag("disco");
        foreach (GameObject projectile in projectiles)
        {
            Destroy(projectile);
        }
    }
}
