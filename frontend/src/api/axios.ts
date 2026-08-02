import axios from "axios";

export const api = axios.create({
  baseURL: "https://growthos-backend-anuz2004.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});