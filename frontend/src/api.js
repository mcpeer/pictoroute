import axios from 'axios';

export const processImages = async (images) => {
  const formData = new FormData();
  images.forEach((image) => formData.append('images', image));

  const response = await axios.post('/process-images', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const refetchCoordinates = async (addresses) => {
  const response = await axios.post('/refetch-coordinates', addresses);
  return response.data;
};

export const getShortestPath = async (addresses) => {
  const response = await axios.post('/get-shortest-path', addresses);
  return response.data;
};
