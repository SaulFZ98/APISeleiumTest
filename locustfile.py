from locust import HttpUser, task, between

class APIUser(HttpUser):                      #HttpUser: representa el usuario simulando trafico HTTP
    wait_time =  between(1,3)  # cada usuario espera entre 1 y 3 segundos entre peticiones


    @task               #esta funcion se ejecuta cada vez que el usuario simulado hace una accion
    def get_users(self):
        self.client.get("/users")  # llama al endpoint /users