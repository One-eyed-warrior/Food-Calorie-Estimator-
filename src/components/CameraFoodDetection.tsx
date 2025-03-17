import React, { useRef, useEffect, useState } from 'react';
import { Camera, Upload, X, Check, Camera as CameraIcon } from 'lucide-react';
import * as cocoSsd from '@tensorflow-models/coco-ssd';
import '@tensorflow/tfjs';

interface CameraFoodDetectionProps {
  onFoodDetected: (foodName: string) => void;
}

export function CameraFoodDetection({ onFoodDetected }: CameraFoodDetectionProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isActive, setIsActive] = useState(false);
  const [model, setModel] = useState<cocoSsd.ObjectDetection | null>(null);
  const [loading, setLoading] = useState(false);
  const [detectedFood, setDetectedFood] = useState<string | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);

  useEffect(() => {
    const loadModel = async () => {
      try {
        const loadedModel = await cocoSsd.load();
        setModel(loadedModel);
      } catch (error) {
        console.error('Error loading model:', error);
      }
    };
    loadModel();
  }, []);

  const startCamera = async () => {
    setLoading(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
        setIsActive(true);
      }
    } catch (error) {
      console.error('Error accessing camera:', error);
      alert('Could not access camera. Please make sure you have granted camera permissions.');
    }
    setLoading(false);
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsActive(false);
      setDetectedFood(null);
      setCapturedImage(null);
    }
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      if (context) {
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0);
        const imageDataUrl = canvasRef.current.toDataURL('image/jpeg');
        setCapturedImage(imageDataUrl);
        detectFoodInImage(canvasRef.current);
      }
    }
  };

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !model) return;

    const img = new Image();
    img.src = URL.createObjectURL(file);
    
    img.onload = async () => {
      try {
        const predictions = await model.detect(img);
        const foodItems = predictions.filter(prediction => 
          ['banana', 'apple', 'orange', 'carrot', 'broccoli', 'sandwich', 'pizza', 'donut', 'cake']
          .includes(prediction.class.toLowerCase())
        );

        if (foodItems.length > 0) {
          setDetectedFood(foodItems[0].class);
        } else {
          alert('No food items detected in the image. Please try another image.');
        }
      } catch (error) {
        console.error('Error detecting objects:', error);
      }
      URL.revokeObjectURL(img.src);
    };
  };

  const detectFoodInImage = async (imageElement: HTMLCanvasElement | HTMLImageElement) => {
    if (!model) return;

    try {
      const predictions = await model.detect(imageElement);
      const foodItems = predictions.filter(prediction => 
        ['banana', 'apple', 'orange', 'carrot', 'broccoli', 'sandwich', 'pizza', 'donut', 'cake']
        .includes(prediction.class.toLowerCase())
      );

      if (foodItems.length > 0) {
        setDetectedFood(foodItems[0].class);
      } else {
        alert('No food items detected. Please try again.');
      }
    } catch (error) {
      console.error('Error detecting objects:', error);
    }
  };

  const handleConfirmFood = () => {
    if (detectedFood) {
      onFoodDetected(detectedFood);
      stopCamera();
      setDetectedFood(null);
      setCapturedImage(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Food Detection</h2>
      
      <div className="space-y-4">
        {/* Camera Controls */}
        <div className="flex gap-2">
          {!isActive ? (
            <>
              <button
                onClick={startCamera}
                disabled={loading}
                className="flex-1 flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <Camera className="w-4 h-4 mr-2" />
                {loading ? 'Loading...' : 'Start Camera'}
              </button>
              
              <label className="flex-1 flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 cursor-pointer">
                <Upload className="w-4 h-4 mr-2" />
                Upload Image
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
              </label>
            </>
          ) : (
            <div className="w-full flex gap-2">
              <button
                onClick={captureImage}
                className="flex-1 flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <CameraIcon className="w-4 h-4 mr-2" />
                Capture Image
              </button>
              <button
                onClick={stopCamera}
                className="flex-1 flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <X className="w-4 h-4 mr-2" />
                Stop Camera
              </button>
            </div>
          )}
        </div>

        {/* Camera Preview */}
        {isActive && !capturedImage && (
          <div className="relative rounded-lg overflow-hidden shadow-lg bg-black">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-auto"
              style={{ minHeight: '300px' }}
            />
            <canvas ref={canvasRef} className="hidden" />
            <div className="absolute top-2 left-2 right-2 bg-black bg-opacity-50 text-white p-2 rounded text-sm text-center">
              Click "Capture Image" when ready to detect food
            </div>
          </div>
        )}

        {/* Captured Image Preview */}
        {capturedImage && (
          <div className="relative rounded-lg overflow-hidden shadow-lg">
            <img
              src={capturedImage}
              alt="Captured food"
              className="w-full h-auto"
              style={{ minHeight: '300px' }}
            />
          </div>
        )}

        {/* Detection Result */}
        {detectedFood && (
          <div className="bg-green-50 border border-green-200 rounded-md p-4">
            <div className="flex items-center justify-between">
              <p className="text-green-800">
                Detected food: <span className="font-semibold">{detectedFood}</span>
              </p>
              <button
                onClick={handleConfirmFood}
                className="flex items-center px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <Check className="w-4 h-4 mr-1" />
                Add Food
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}