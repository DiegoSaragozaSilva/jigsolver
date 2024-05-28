import React, { useState } from "react";
import { useTheme } from "@mui/material/styles";

interface ImagePreviewProps {
  file: File | null;
}

const ImagePreview: React.FC<ImagePreviewProps> = ({ file }) => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const theme = useTheme();

  // Effect to handle new file objects
  React.useEffect(() => {
    if (file) {
      const url = URL.createObjectURL(file);
      setImageUrl(url);

      // Clean up the URL when the component unmounts or file changes
      return () => URL.revokeObjectURL(url);
    }
  }, [file]);

  if (!file) {
    return <div>No image selected</div>;
  }

  return (
    <div
      style={{
        width: "80%",
        height: "50%",
        margin: theme.spacing(2),
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <img
        src={imageUrl || ""}
        alt="Preview"
        style={{
          maxWidth: "100%",
          maxHeight: "100%",
        }}
      />
    </div>
  );
};

export default ImagePreview;
