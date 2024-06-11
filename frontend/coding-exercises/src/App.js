// Simple Frontend with an input text field and an output text field
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');
    const [diagram, setDiagram] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // Send a POST request to the FastAPI backend
            const result = await axios.post('http://127.0.0.1:8000/generate', {
                prompt: prompt
            });
            // Set the response from the backend
            setResponse(result.data.response);
        } catch (error) {
            console.error('Error generating response:', error);
        }
    };

    const handleConvertToDiagram = async () => {
        try {
            // Send a POST request to fetch the PNG image from the backend
            const result = await axios.post('http://127.0.0.1:8000/convert-to-diagram', {}, {
                responseType: 'blob'
            });
            // Create a URL for the fetched blob object
            const imageUrl = URL.createObjectURL(result.data);
            // Set the URL as the source for the image
            setDiagram(imageUrl);
        } catch (error) {
            console.error('Error converting to diagram:', error);
        }
    };

    return (
        <div className="App">
            <div className="content">
                <div className="form-container">
                    <form onSubmit={handleSubmit}>
                        <div className="input-container">
                            <label htmlFor="prompt">Prompt:</label>
                            <textarea 
                                id="prompt"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)} 
                                placeholder="Enter your description here"
                            />
                        </div>
                        <button type="submit">Generate PlantUML code</button>
                    </form>
                    <div className="response-container">
                        <label htmlFor="response">Response:</label>
                        <textarea
                            id="response"
                            value={response}
                            readOnly
                        />
                    </div>
                    <button onClick={handleConvertToDiagram}>Convert to PNG diagram</button>
                </div>
                {diagram && (
                    <div className="diagram-container">
                        <img src={diagram} alt="Diagram" />
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
