import React, { useState, useCallback } from "react";
import { ThemeProvider } from "@mui/material/styles";
import { ReactNotifications, Store } from "react-notifications-component";
import "react-notifications-component/dist/theme.css";

import { sendImage } from "./clients/backendClient";

import draculaTheme from "./theme";
import Header from "./components/Header";
import PageWrapper from "./components/PageWrapper";
import SectionWrapper from "./components/SectionWrapper";
import DragAndDropUpload from "./components/DragAndDropUpload";
import ImagePreview from "./components/ImagePreview";
import SendButton from "./components/SendButton";
import Loading from "./components/Loading";
import ImagePopup from "./components/ImagePopup";
import SliderControl from "./components/SliderControl";

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [imageUrl, setImageUrl] = useState<string>("");
  const [distanceThreshold, setDistanceThreshold] = useState<number>(150); // State for the distance threshold

  const onClosePopup = useCallback(() => {
    setImageUrl("");
  }, []);

  const addNotification = useCallback(
    (title: string, message: string, type: "danger" | "success") => {
      Store.addNotification({
        title,
        message,
        type,
        insert: "top",
        container: "top-right",
        animationIn: ["animate__animated", "animate__fadeIn"],
        animationOut: ["animate__animated", "animate__fadeOut"],
        dismiss: {
          duration: 2000,
          onScreen: true,
        },
      });
    },
    []
  );

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 1) {
        addNotification(
          "Error!",
          "You can only upload one file at a time",
          "danger"
        );
        return;
      }

      if (!acceptedFiles[0].type.includes("image")) {
        addNotification("Error!", "You can only upload images", "danger");
        return;
      }
      setFile(acceptedFiles[0]);
    },
    [addNotification]
  );

  const onSend = useCallback(() => {
    setLoading(true);
    setTimeout(() => {
      sendImage(file!, distanceThreshold) // Updated to include distanceThreshold
        .then((receivedImageUrl) => {
          setImageUrl(receivedImageUrl);
          addNotification("Success!", "Image sent successfully", "success");
        })
        .catch((error) => {
          addNotification(
            "Error!",
            "Try to configure another distance threshold",
            "danger"
          );
        })
        .finally(() => {
          setLoading(false);
        });
    }, 5000);
  }, [file, distanceThreshold]); // Include distanceThreshold in dependency array

  return (
    <div>
      <ReactNotifications />
      <ThemeProvider theme={draculaTheme}>
        <Header />
        <PageWrapper height="calc(100vh - 64px)">
          {loading ? (
            <Loading />
          ) : (
            <SectionWrapper flexDirection="row" alignItems="center">
              <DragAndDropUpload onDrop={onDrop} />
              {file && <ImagePreview file={file} />}
            </SectionWrapper>
          )}
          {!loading && file && (
            <SectionWrapper
              flexDirection="column"
              alignItems="center"
              marginTop="-10%"
              gap="5%"
            >
              <SliderControl
                label="Insert the approximate size of the piece in pixels"
                value={distanceThreshold}
                onChange={setDistanceThreshold}
              />
              <SendButton onSend={onSend} file={file} />
            </SectionWrapper>
          )}
        </PageWrapper>
        {imageUrl && <ImagePopup imageUrl={imageUrl} onClose={onClosePopup} />}
      </ThemeProvider>
    </div>
  );
};

export default App;
