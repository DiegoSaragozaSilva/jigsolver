import axios from "axios";

const apiUrl = "http://localhost:8000/solve-jigsaw/";

export const sendImage = async (
  file: File,
  distanceThreshold: number = 150
): Promise<string> => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(apiUrl, formData, {
      params: {
        distance_threshold: distanceThreshold,
      },
      headers: {
        "Content-Type": "multipart/form-data",
      },
      responseType: "blob", // Important for handling binary data like images
    });
    return URL.createObjectURL(response.data);
  } catch (error: any) {
    throw new Error(error.response?.data || "Unknown error occurred");
  }
};
