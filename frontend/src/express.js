import express from 'express';

const app = express(); 
app.use(express.static("build"));

app.listen(5173, () => {
	console.log("Frontend server started on port 5173");
});