# Coverage Zone Visualizer for Rugged Terrain

**Problem**: when installing radio link antennas in rugged terrain, it is necessary to determine the antenna coverage considering:

- antenna and receiver equipment height
- Fresnel zone
- distance between the antenna and the receiver

**Scope**: simplify the work of radio link coverage analysts.

![alt text](image.png)


## deploy

- decrypt envs
```sh
SOPS_AGE_KEY_FILE=../key.txt sops decrypt enc.env > .env
```
- build project locally
```sh
docker compose up --build
```

- go to `localhost:3000/seed` to populate the first intial user
- go to `localhost:3000` and fill the credencials user `user@example.com` and password `password123`


## develop

encrypt the envs
```sh
sops encrypt --age PUBLIC_KEY .env > enc.env
```
