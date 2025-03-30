using System.Collections;
using UnityEngine;

public class ProjectileSpawner : MonoBehaviour
{
    public GameObject projectilePrefab;
    public Transform spawnPoint;
    public float spawnInterval = 4f;
    public float moveSpeed = 2f;
    private void Start()
    {
        StartCoroutine(SpawnProjectiles());
    }
    IEnumerator SpawnProjectiles()
    {
        while (true)
        {
            GameObject projectile = Instantiate(projectilePrefab, new Vector3(7f, spawnPoint.position.y, spawnPoint.position.z), Quaternion.identity);
            StartCoroutine(MoveProjectile(projectile));
            yield return new WaitForSeconds(spawnInterval);
        }
    }
    IEnumerator MoveProjectile(GameObject projectile)
    {
        while (projectile != null && projectile.transform.position.z > -4f)
        {
            projectile.transform.position -= new Vector3(moveSpeed * Time.deltaTime,0,0);
            yield return null;
        }
        if (projectile != null)
        {
            Destroy(projectile);
            StartCoroutine(SpawnProjectiles()); // Respawn a new projectile
        }
    }
}
