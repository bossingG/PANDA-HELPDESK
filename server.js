const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 8080;

app.use(bodyParser.urlencoded({ extended: true }));

// I-serve ang HTML interface ng form
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// DIRECT AT KUMPLETONG PAGSASALO NG DATA
app.post('/submit-concern', (req, res) => {
    const { Full_Name, Rider_ID, Rider_Email, Concern_Message } = req.body;
    
    // Dito sa logEntry siguradong kasama na ang LAHAT ng input nila
    const logEntry = `
=========================================
Petsa/Oras   : ${new Date().toLocaleString('en-US', { timeZone: 'Asia/Manila' })}
Rider Name   : ${Full_Name}
Rider ID     : ${Rider_ID}
Rider Email  : ${Rider_Email}
Concern Text : ${Concern_Message}
=========================================\n`;

    // Isusulat nang buo sa local text file
    fs.appendFile(path.join(__dirname, 'concerns.txt'), logEntry, (err) => {
        if (err) {
            console.error('Error sa pag-save:', err);
            return res.status(500).send('May error ang backend server.');
        }
        
        console.log(`[SUCCESS] Kumpletong detalye ni Rider ID: ${Rider_ID} ay ligtas na na-save!`);
        
        // MAKATOTOHANANG SUCCESS PAGE (MATINGKAD AT PROFESSIONAL DARK THEME)
        res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Success - Concern Submitted</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: sans-serif; background-color: #121212; color: #e0e0e0; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 20px; }
                .success-card { background-color: #1f1f1f; max-width: 400px; width: 100%; padding: 30px 20px; border-radius: 16px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.5); border-top: 4px solid #e21b70; }
                .icon { font-size: 3rem; color: #e21b70; margin-bottom: 15px; }
                h1 { font-size: 1.3rem; color: #ffffff; margin-bottom: 10px; font-weight: normal; }
                p { font-size: 0.9rem; color: #aaa; margin-bottom: 25px; line-height: 1.4; }
                .back-btn { display: inline-block; width: 100%; background-color: #e21b70; color: #fff; text-decoration: none; padding: 14px; font-size: 0.95rem; font-weight: bold; border-radius: 8px; transition: background 0.2s; }
                .back-btn:hover { background-color: #c1125d; }
            </style>
        </head>
        <body>
            <div class="success-card">
                <div class="icon">✓</div>
                <h1>submitted successfully</h1>
                <p>Ang iyong rider ticket ay direktang naipadala at nairehistro na sa aming internal helpdesk system.</p>
                <a href="/" class="back-btn">Gumawa ng Bagong Ticket</a>
            </div>
        </body>
        </html>
        `);
    });
});

app.listen(PORT, () => {
    console.log(`Server running direct at http://localhost:${PORT}`);
});
