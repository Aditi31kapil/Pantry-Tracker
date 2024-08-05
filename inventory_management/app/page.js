'use client'
import { storage } from '@/firebase'; // Ensure this import is correct
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import Image from "next/image"
import { useState, useEffect,useRef } from 'react'
import { firestore } from '@/firebase'
import { Box, Modal, Typography, Stack, TextField, Button,IconButton, MenuItem, Select, InputLabel, FormControl } from "@mui/material"
import { collection, deleteDoc, doc, getDocs, query, getDoc, setDoc, updateDoc } from "firebase/firestore"
import styles from './page.module.css'
import {Camera} from "react-camera-pro";
import React from 'react';
import CloseIcon from '@mui/icons-material/Close';



export default function Home() {
  const camera = useRef(null);
  const [isCameraOpen, setIsCameraOpen] = React.useState(false);
  const [inventory, setInventory] = useState([]);
  const [open, setOpen] = useState(false);
  const [itemName, setItemName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [category, setCategory] = useState('');
  const [photo, setPhoto] = useState(null);
  const [search, setSearch] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedItems, setSelectedItems] = useState([]);
  const [servings, setServings] = useState(1);
  const [recipe, setRecipe] = useState(null);


  const updateInventory = async () => {
    const snapshot = query(collection(firestore, 'inventory'));
    const docs = await getDocs(snapshot);
    const inventoryList = [];
    docs.forEach((doc) => {
      inventoryList.push({
        name: doc.id,
        ...doc.data(),
      });
    });
    setInventory(inventoryList);
  };

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setPhoto(e.target.files[0]);
    }
  };
  const handleTakePhoto = async () => {
    const image = await camera.current.takePhoto({
      // Specify JPG format here if your library supports it
      format: 'image/jpeg', // Example, adjust based on your library
      quality: 0.8 // Optional: Adjust quality (0.0 - 1.0)
    });
    if (image) {
      setPhoto(image);
    }
    setIsCameraOpen(false); // Close camera after taking photo
  };

  const handleCloserecipe = () => {
    setSelectedItems([]);
    setServings(1);
    setRecipe(null);
  };

  const addItem = async () => {
    if (!itemName || !quantity || !price || !category || !photo) return;

    const photoRef = ref(storage, `images/${photo.name}`);
    await uploadBytes(photoRef, photo);
    const photoURL = await getDownloadURL(photoRef);

    const docRef = doc(collection(firestore, 'inventory'), itemName);
    await setDoc(docRef, {
      quantity: parseInt(quantity),
      price: parseFloat(price),
      category,
      photo: photoURL
    });
    await updateInventory();
    setItemName('');
    setQuantity('');
    setPrice('');
    setCategory('');
    setPhoto(null);
    handleClose();
  };

  const editItem = async () => {
    if (!itemName) return;

    const docRef = doc(collection(firestore, 'inventory'), itemName);

    const updates = {};
    if (quantity) updates.quantity = parseInt(quantity);
    if (price) updates.price = parseFloat(price);
    if (category) updates.category = category;
    if (photo) {
      const photoRef = ref(storage, `images/${photo.name}`);
      await uploadBytes(photoRef, photo);
      const photoURL = await getDownloadURL(photoRef);
      updates.photo = photoURL;
    }

    await updateDoc(docRef, updates);
    await updateInventory();
    setItemName('');
    setQuantity('');
    setPrice('');
    setCategory('');
    setPhoto(null);
    handleClose();
  };

  const removeItem = async (item) => {
    const docRef = doc(collection(firestore, 'inventory'), item);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      const { quantity } = docSnap.data();
      if (quantity === 1) {
        await deleteDoc(docRef);
        removeFromUI(item);
      } else {
        await setDoc(docRef, { quantity: quantity - 1 }, { merge: true });
      }
    }
    await updateInventory();
  };
  // Function to remove the item from the UI
  const removeFromUI = (item) => {
  const itemElement = document.getElementById(itemName); // Assuming each item has a unique ID
  if (itemElement) {
      itemElement.remove(); // Remove the item element from the DOM
  }
};

  useEffect(() => {
    updateInventory();
  }, []);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  ;
  const { GoogleGenerativeAI } = require("@google/generative-ai");
  const genAI = new GoogleGenerativeAI("AIzaSyB9BJ38XwV1GFkkZTsp9rfTEG7IZP5ww5Q");

  const generateRecipe = async () =>{  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    const items = selectedItems.map(item => `${item.name}: ${item.price} per kg`).join(', ');
    const prompt = `Generate a recipe for ${servings} servings using the following ingredients: ${items}. Write this recipe in steps and also estimate the price in ruppees of the dish according to the weight of items used at the end. give the answer in the format:
    1) Name of Dish: 
    2) Ingredients used with quantity:
    3) Steps of preparing recipe: 
    4) Estimated cost:`;

    const result = await model.generateContent(prompt);
    const response = result.response;
    if (!response) {
      throw new Error('Response is null');
    }

    const text = await response.text();
    if (!text) {
      throw new Error('Response text is null');
    }

    // Remove unwanted characters
    const cleanText = text.replace(/[/*#]/g, '');

    // Extract and format the output
    const lines = cleanText.split('\n').filter(line => line.trim() !== '');
    let recipeName = "Recipe";
    let ingredients = "";
    let steps = "";
    let estimatedCost = "";

    let isIngredients = false;
    let isSteps = false;
    let isEstimatedCost = false;

    lines.forEach(line => {
      if (line.toLowerCase().includes("ingredients")) {
        isIngredients = true;
        isSteps = false;
        isEstimatedCost = false;
      } else if (line.toLowerCase().includes("steps") || line.toLowerCase().includes("method")) {
        isIngredients = false;
        isSteps = true;
        isEstimatedCost = false;
      } else if (line.toLowerCase().includes("estimated cost") || line.toLowerCase().includes("price")) {
        isIngredients = false;
        isSteps = false;
        isEstimatedCost = true;
      } else {
        if (isIngredients) {
          ingredients += line.trim() + '\n';
        } else if (isSteps) {
          steps += line.trim() + '\n';
        } else if (isEstimatedCost) {
          estimatedCost += line.trim();
        } else if (!isIngredients && !isSteps && !isEstimatedCost) {
          // Assume the first line is the recipe name
          recipeName = line.trim();
        }
      }
    });

    const formattedRecipe = `
      Name of Recipe: ${recipeName}

      Ingredients:
      ${ingredients}

      Steps to make the dish:
      ${steps}

      Estimated cost:
      ${estimatedCost}
    `;

    setRecipe(formattedRecipe);
  } catch (error) {
    console.error("Error generating recipe:", error.message);
    setRecipe("An error occurred while generating the recipe. Please try again.");
  }
};
    //const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
  
  //   const items = selectedItems.map(item => `${item.name}: ${item.price} per kg`).join(', ');
  //   const prompt = `Generate a recipe for ${servings} servings using the following ingredients: ${items}. Write this recipe in steps and also estimate the price in ruppees of the dish according to the weight of items used at the end. give the answer in the format:
  //   1) Name of Dish: 
  //   2) Ingredients used with quantity:
  //   3) Steps of preparing recipe: 
  //   4) Estimated cost:`;
  
  //   const result = await model.generateContent(prompt);
  //   const response = await result.response;
  //   const text = response.text();
  
  //   // Remove unwanted characters
  //   const cleanText = text.replace(/[/*#]/g, '');
  //   setRecipe(cleanText);
  // };
  

  const uniqueCategories = [...new Set(inventory.map(item => item.category))];

  const filteredInventory = inventory.filter(item => {
    const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
    const matchesSearch = item.name.toLowerCase().includes(search.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <Box className={styles.container}>
      <Modal open={open} onClose={handleClose}>
  <Box className={styles.modal}>
    <Stack direction="row" justifyContent="space-between" alignItems="center">
      <Typography variant="h6">{isEditing ? 'Edit Item' : 'Add Item'}</Typography>
      <IconButton onClick={handleClose}>
        <CloseIcon />
      </IconButton>
    </Stack>
    <Stack spacing={2}>
      <TextField
        label="Item Name"
        variant='outlined'
        fullWidth
        value={itemName}
        onChange={(e) => setItemName(e.target.value)}
        disabled={isEditing}
      />
      <TextField
        label="Quantity"
        variant='outlined'
        fullWidth
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
      />
      <TextField
        label="Price (INR)"
        variant='outlined'
        fullWidth
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      />
      <FormControl fullWidth>
        <InputLabel>Category</InputLabel>
        <Select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <MenuItem value="Fruits">Fruits</MenuItem>
          <MenuItem value="Vegetables">Vegetables</MenuItem>
          <MenuItem value="Spices">Spices</MenuItem>
          <MenuItem value="Non-Veg">Non-Veg</MenuItem>
          <MenuItem value="Dairy Products">Dairy Products</MenuItem>
        </Select>
      </FormControl>
      <Stack space={2}>
      {isCameraOpen && <Camera ref={camera} />}
      <Button
        variant="contained"
        component="label"
        onClick={() => setIsCameraOpen(true)} // Open camera on button click
      >
        Take Photo 
        </Button>
          {isCameraOpen && (
            <Button
              variant="contained"
              padding-top="2px"
              onClick={handleTakePhoto} // Handle photo taking
            >
              Capture Photo
            </Button>
          )}
        </Stack>
      <Button
        variant="contained"
        component="label"
      >
        Upload Photo
        <input
          type="file"
          accept="image/jpeg,image/png"
          hidden
          onChange={handleFileChange}
        />
      </Button>
      <Button
        variant="outlined"
        onClick={isEditing ? editItem : addItem}
      >
        {isEditing ? 'Update' : 'Add'}
      </Button>
    </Stack>
   </Box>
  </Modal>
      <Box className={styles.header}>
        <Typography variant="h2" className={styles.title}>
          Inventory Items
        </Typography>
        <Box display="flex" alignItems="center" gap={2}>
          <TextField
            label="Search"
            variant="outlined"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <Button variant="contained" onClick={handleOpen}>
            Add New Item
          </Button>
        </Box>
      </Box>
      <Stack direction="row" spacing={2} marginBottom={2}>
        <Button variant={selectedCategory === 'All' ? 'contained' : 'outlined'} onClick={() => setSelectedCategory('All')}>
          All Items
        </Button>
        {uniqueCategories.map((cat) => (
          <Button 
            key={cat} 
            variant={selectedCategory === cat ? 'contained' : 'outlined'} 
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </Button>
        ))}
      </Stack>
      <Box className={styles.selecteditemBox} display="flex" alignItems="center" gap={3} justifyContent="center">
        <Typography variant="h5" >Selected Items</Typography>
        {selectedItems.map(({ name, price }) => (
          <Box key={name} className={styles.selectedItem}>
            <Typography>{name} - {price} per kg</Typography>
          </Box>
        ))}
        <TextField className={styles.search}
          placeholder="Servings"
          variant="outlined"
          type="number"
          value={servings}
          onChange={(e) => setServings(e.target.value)}
        />
        <Button variant="contained" onClick={generateRecipe}>Generate Recipe</Button>
      </Box>
      <Box className={styles.Modal}>
      {recipe && (
        <Box className={styles.recipe}>
          <Typography variant="h5">Recipe
          <IconButton onClick={handleCloserecipe}>
          <CloseIcon />
          </IconButton>
          </Typography>
          <Typography variant="body1">{recipe}</Typography>
        </Box>
      )}
      </Box>
      <Stack className={styles.inventoryList}>
        {filteredInventory.map(({ name, quantity, price, category, photo }) => (
          <Box key={name} className={`${styles.inventoryItem} ${quantity < 5 ? styles.lowStock : ''}`}>
            <Image 
              src={photo}
              alt={name} 
              width={100} 
              height={100} 
            />
            <Box>
              <Typography variant='h5' className={styles.itemName}>
                <u>{name.charAt(0).toUpperCase() + name.slice(1)}</u>
              </Typography>
              <Typography variant='body1'>
                Quantity: {quantity}
              </Typography>
              <Typography variant='body1'>
                Price: ₹{price}
              </Typography>
              <Typography variant='body1'>
                Category: {category}
              </Typography>
            </Box>
            <Button variant="contained" color="error" onClick={() => removeItem(name)}>
              Remove
            </Button>
            <Button
              variant="contained"
              color="success"
              onClick={() => {
                setItemName(name);
                setQuantity(quantity);
                setPrice(price);
                setCategory(category);
                setPhoto(null);
                setIsEditing(true);
                handleOpen();
              }}
            >
              Edit Item
            </Button>
            <Button
              variant="contained"
              onClick={() => {
                const selectedItem = { name, quantity: 1, price };
                setSelectedItems([...selectedItems, selectedItem]);
              }}
            >
              Select Item
            </Button>
          </Box>
        ))}
      </Stack>
    </Box>
  );
}
