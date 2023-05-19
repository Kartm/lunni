import defaultAxios from "axios";

export const axios = defaultAxios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-type": "application/json",
  },
});
