// Image Display Component for AI Tutor
// Funky, kid-themed image display with extracted words

class ImageDisplayComponent {
    constructor() {
        this.currentImage = null;
        this.currentWord = null;
        this.animationTimeout = null;
        this.init();
    }

    init() {
        this.createImageContainer();
        this.setupStyles();
    }

    createImageContainer() {
        // Create the main image display container
        const imageContainer = document.createElement('div');
        imageContainer.id = 'imageDisplayContainer';
        imageContainer.className = 'image-display-container hidden';

        imageContainer.innerHTML = `
            <div class="image-display-content">

                <div class="image-wrapper">
                    <div class="image-frame">
                        <img id="generatedImage" src="" alt="Generated visual" class="generated-image">
                        <div class="image-sparkles">
                            <span class="sparkle">✨</span>
                            <span class="sparkle">⭐</span>
                            <span class="sparkle">🌟</span>
                            <span class="sparkle">💫</span>
                        </div>
                    </div>
                </div>

                <div class="word-display">
                    <div class="word-bubble">
                        <span class="featured-word" id="featuredWord"></span>
                    </div>
                </div>

            </div>
        `;

        // Insert into the right side area
        const rightSide = document.querySelector('.right-side');
        if (rightSide) {
            rightSide.appendChild(imageContainer);
        } else {
            // Fallback: insert after main container
            const mainContainer = document.querySelector('.main-container');
            mainContainer.appendChild(imageContainer);
        }
    }

    setupStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .image-display-container {
                position: relative;
                width: 100%;
                height: 100%;
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 100;
                transition: all 0.5s ease;
            }

            .image-display-container.hidden {
                opacity: 0;
                pointer-events: none;
                transform: scale(0.8) translateX(50px);
            }

            .image-display-content {
                background: linear-gradient(135deg, #FFE135, #FF6B6B, #4ECDC4, #45B7D1);
                border-radius: 25px;
                padding: 30px;
                max-width: 450px;
                width: 100%;
                text-align: center;
                position: relative;
                animation: bounceIn 0.8s ease;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }

            .bouncy-header {
                margin-bottom: 20px;
            }

            .bouncy-header h3 {
                color: white;
                font-size: 1.8rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                animation: wiggle 2s infinite;
            }

            .image-wrapper {
                margin: 20px 0;
                position: relative;
            }

            .image-frame {
                position: relative;
                background: white;
                border-radius: 20px;
                padding: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transform: rotate(-2deg);
                transition: transform 0.3s ease;
            }

            .image-frame:hover {
                transform: rotate(0deg) scale(1.05);
            }

            .generated-image {
                width: 100%;
                max-width: 280px;
                height: 280px;
                object-fit: cover;
                border-radius: 15px;
                display: block;
                margin: 0 auto;
            }

            .image-sparkles {
                position: absolute;
                top: -10px;
                right: -10px;
                animation: sparkleFloat 3s infinite;
            }

            .sparkle {
                display: inline-block;
                font-size: 1.2rem;
                animation: sparkleRotate 2s infinite linear;
                margin: 0 2px;
            }

            .word-display {
                margin: 25px 0;
            }

            .word-bubble {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 20px;
                padding: 20px;
                display: inline-block;
                position: relative;
                animation: pulse 2s infinite;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }

            .word-bubble::before {
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                border: 10px solid transparent;
                border-top-color: rgba(255, 255, 255, 0.9);
            }

            .featured-word {
                font-size: 2.5rem;
                font-weight: bold;
                color: #FF6B6B;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                display: block;
                margin-bottom: 5px;
            }

            .word-phonetic {
                font-size: 1.1rem;
                color: #666;
                font-style: italic;
            }


            /* Animations */
            @keyframes bounceIn {
                0% {
                    opacity: 0;
                    transform: scale(0.3) rotate(-10deg);
                }
                50% {
                    opacity: 1;
                    transform: scale(1.1) rotate(5deg);
                }
                100% {
                    opacity: 1;
                    transform: scale(1) rotate(0deg);
                }
            }

            @keyframes wiggle {
                0%, 100% { transform: rotate(0deg); }
                25% { transform: rotate(1deg); }
                75% { transform: rotate(-1deg); }
            }

            @keyframes sparkleFloat {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }

            @keyframes sparkleRotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }

            /* Mobile responsiveness */
            @media (max-width: 1024px) {
                .image-display-container {
                    margin-top: 1rem;
                    min-height: 300px;
                }
            }

            @media (max-width: 768px) {
                .image-display-content {
                    padding: 20px;
                    margin: 10px 0;
                }

                .bouncy-header h3 {
                    font-size: 1.4rem;
                }

                .featured-word {
                    font-size: 2rem;
                }

                .image-display-container {
                    min-height: 250px;
                }
            }
        `;
        document.head.appendChild(style);
    }


    // Show the image display with animation
    async showImage(response, imageUrl) {
        const container = document.getElementById('imageDisplayContainer');
        const imageElement = document.getElementById('generatedImage');
        const wordElement = document.getElementById('featuredWord');

        // Extract featured word
        const featuredWord = response.highlight_word;


        // Set the content
        imageElement.src = imageUrl;
        wordElement.textContent = featuredWord;

        // Store current data
        this.currentImage = imageUrl;
        this.currentWord = featuredWord;

        // Show with animation
        container.classList.remove('hidden');

        // Setup event listeners
        this.setupEventListeners();

        // Auto-hide after 10 seconds if not manually closed
        this.animationTimeout = setTimeout(() => {
            this.hideImage();
        }, 10000);
    }

    // Hide the image display
    hideImage() {
        const container = document.getElementById('imageDisplayContainer');
        container.classList.add('hidden');

        if (this.animationTimeout) {
            clearTimeout(this.animationTimeout);
            this.animationTimeout = null;
        }
    }

    // Setup event listeners for buttons
    setupEventListeners() {
        const speakBtn = document.getElementById('speakWordBtn');
        const closeBtn = document.getElementById('closeImageBtn');

        // Remove existing listeners to prevent duplicates
        speakBtn.replaceWith(speakBtn.cloneNode(true));
        closeBtn.replaceWith(closeBtn.cloneNode(true));

        // Add new listeners
        document.getElementById('speakWordBtn').addEventListener('click', () => {
            this.speakWord();
        });

        document.getElementById('closeImageBtn').addEventListener('click', () => {
            this.hideImage();
        });

        // Close on background click
        document.getElementById('imageDisplayContainer').addEventListener('click', (e) => {
            if (e.target.id === 'imageDisplayContainer') {
                this.hideImage();
            }
        });
    }

    // Speak the featured word using text-to-speech
    speakWord() {
        if (this.currentWord && 'speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(this.currentWord);
            utterance.rate = 0.8;
            utterance.pitch = 1.2;
            speechSynthesis.speak(utterance);
        }
    }

    // Public method to trigger image display
    displayImageForResponse(response, imageUrl) {
        this.showImage(response, imageUrl);
    }
}

// Initialize the component when DOM is loaded
let imageDisplayComponent;
document.addEventListener('DOMContentLoaded', function() {
    imageDisplayComponent = new ImageDisplayComponent();
    window.imageDisplayComponent = imageDisplayComponent;
});

// Export for use in other scripts
window.ImageDisplayComponent = ImageDisplayComponent;
