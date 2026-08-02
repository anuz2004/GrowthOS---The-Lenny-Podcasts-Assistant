import axios from "axios";

export const api = axios.create({
  baseURL: "https://growthos-backend-anuz2004.onrender.com/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});