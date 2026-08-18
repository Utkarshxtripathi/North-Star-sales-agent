document.addEventListener("DOMContentLoaded", () => {
    // Retrieve existing session ID or generate a new random session key
    let sessionId = sessionStorage.getItem("northstar_session_id");
    if (!sessionId) {
        sessionId = "sess_" + Math.random().toString(36).substring(2, 9);
        sessionStorage.setItem("northstar_session_id", sessionId);
    }

    // Chat and navigation DOM elements
    const sessionDisplay = document.getElementById("sessionDisplay");
    const chatViewport = document.getElementById("chatViewport");
    const chatForm = document.getElementById("chatForm");
    const userInput = document.getElementById("userInput");
    const btnSend = document.getElementById("btnSend");
    const btnMic = document.getElementById("btnMic");
    const btnNewSession = document.getElementById("btnNewSession");
    const typingIndicator = document.getElementById("typingIndicator");
    const ttsToggle = document.getElementById("ttsToggle");

    // CRM intelligence drawer DOM elements
    const btnOpenAnalytics = document.getElementById("btnOpenAnalytics");
    const btnCloseDrawer = document.getElementById("btnCloseDrawer");
    const analyticsDrawer = document.getElementById("analyticsDrawer");
    const analyticsBackdrop = document.getElementById("analyticsBackdrop");
    const btnGenerateAnalytics = document.getElementById("btnGenerateAnalytics");
    const btnCopyJson = document.getElementById("btnCopyJson");
    const analyticsBadgeCount = document.getElementById("analyticsBadgeCount");
    const analyticsPlaceholder = document.getElementById("analyticsPlaceholder");
    const analyticsDetails = document.getElementById("analyticsDetails");

    // Analytics metrics display elements
    const metricInterest = document.getElementById("metricInterest");
    const metricLanguage = document.getElementById("metricLanguage");
    const metricConfig = document.getElementById("metricConfig");
    const metricBudget = document.getElementById("metricBudget");
    const metricSiteVisitStatus = document.getElementById("metricSiteVisitStatus");
    const metricSiteVisitDetails = document.getElementById("metricSiteVisitDetails");
    const metricFollowup = document.getElementById("metricFollowup");
    const metricCallbackTime = document.getElementById("metricCallbackTime");
    const metricSentiment = document.getElementById("metricSentiment");
    const metricObjectionsList = document.getElementById("metricObjectionsList");
    const metricSummary = document.getElementById("metricSummary");
    const metricAction = document.getElementById("metricAction");
    const rawJsonBlock = document.getElementById("rawJsonBlock");

    // Render active session identifier in UI toolbar
    if (sessionDisplay) sessionDisplay.textContent = sessionId;

    // Open slide-over analytics drawer
    function openDrawer() {
        analyticsDrawer.classList.add("open");
        analyticsBackdrop.classList.remove("hidden");
        document.body.style.overflow = "hidden";
    }

    // Close slide-over analytics drawer
    function closeDrawer() {
        analyticsDrawer.classList.remove("open");
        analyticsBackdrop.classList.add("hidden");
        document.body.style.overflow = "";
    }

    // Attach drawer toggle listeners
    if (btnOpenAnalytics) btnOpenAnalytics.addEventListener("click", openDrawer);
    if (btnCloseDrawer) btnCloseDrawer.addEventListener("click", closeDrawer);
    if (analyticsBackdrop) analyticsBackdrop.addEventListener("click", closeDrawer);

    // Close drawer when Escape key is pressed
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && analyticsDrawer.classList.contains("open")) {
            closeDrawer();
        }
    });

    // Populate browser synthesis voices
    let availableVoices = [];
    function initVoices() {
        if ('speechSynthesis' in window) {
            availableVoices = window.speechSynthesis.getVoices();
        }
    }
    initVoices();
    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = initVoices;
    }

    // Select natural voice tailored for Hindi or Indian English
    function getConsistentVoice(isHindi) {
        if (!availableVoices || availableVoices.length === 0) {
            availableVoices = window.speechSynthesis.getVoices();
        }

        if (isHindi) {
            return availableVoices.find(v => (v.lang === 'hi-IN' || v.lang.startsWith('hi')) && (v.name.includes('Female') || v.name.includes('Swara') || v.name.includes('Kalpana') || v.name.includes('Google')))
                || availableVoices.find(v => v.lang.startsWith('hi'))
                || availableVoices.find(v => v.lang.includes('IN'));
        } else {
            return availableVoices.find(v => (v.lang === 'en-IN' || v.lang.includes('en-IN')) && (v.name.includes('Heera') || v.name.includes('Neerja') || v.name.includes('Female') || v.name.includes('Natural') || v.name.includes('Google')))
                || availableVoices.find(v => v.lang.includes('en-IN'))
                || availableVoices.find(v => (v.name.includes('Female') || v.name.includes('Zira') || v.name.includes('Samantha') || v.name.includes('Jenny')) && v.lang.startsWith('en'))
                || availableVoices.find(v => v.lang.startsWith('en'))
                || availableVoices[0];
        }
    }

    // Synthesize spoken audio for assistant responses via Web Speech API
    function speakText(text) {
        if (!('speechSynthesis' in window) || (ttsToggle && !ttsToggle.checked)) return;

        window.speechSynthesis.cancel();
        const cleanText = text.replace(/[*_#`~]/g, '');
        const utterance = new SpeechSynthesisUtterance(cleanText);

        const hasHindiScript = /[\u0900-\u097F]/.test(cleanText);
        utterance.lang = hasHindiScript ? 'hi-IN' : 'en-IN';

        const chosenVoice = getConsistentVoice(hasHindiScript);
        if (chosenVoice) {
            utterance.voice = chosenVoice;
        }

        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        window.speechSynthesis.speak(utterance);
    }

    // Render a chat message bubble, metadata timestamp, and optional tool callout card
    function appendMessage(role, content, toolDetails = null) {
        const group = document.createElement("div");
        group.className = `message-group ${role === 'user' ? 'user-group' : 'assistant-group'}`;

        const avatar = document.createElement("div");
        avatar.className = `avatar ${role === 'user' ? 'user-avatar' : 'advisor-avatar'}`;
        avatar.innerHTML = `<span>${role === 'user' ? 'U' : '✦'}</span>`;

        const bubbleContainer = document.createElement("div");
        bubbleContainer.className = "bubble-container";

        const meta = document.createElement("div");
        meta.className = "bubble-meta";
        meta.innerHTML = `
            <span class="sender-name">${role === 'user' ? 'You' : 'Northstar One AI Advisor'}</span>
            <span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
        `;
        bubbleContainer.appendChild(meta);

        const bubble = document.createElement("div");
        bubble.className = `bubble ${role === 'user' ? 'user-bubble' : 'assistant-bubble'}`;

        const paragraphs = content.split("\n\n").filter(p => p.trim().length > 0);
        if (paragraphs.length > 0) {
            paragraphs.forEach(p => {
                const pElem = document.createElement("p");
                pElem.textContent = p.replace(/\*\*/g, '');
                bubble.appendChild(pElem);
            });
        } else {
            const pElem = document.createElement("p");
            pElem.textContent = content;
            bubble.appendChild(pElem);
        }

        // Render tool execution badge if a function call was made
        if (toolDetails) {
            const isSuccess = toolDetails.response && toolDetails.response.status === 'success';
            const toolCard = document.createElement("div");
            toolCard.className = `tool-callout ${isSuccess ? 'success' : 'failure'}`;

            let detailsText = '';
            if (isSuccess) {
                detailsText = `Booking ID: ${toolDetails.response.booking_id || 'Confirmed'} • Slot: ${toolDetails.response.date || ''} at ${toolDetails.response.time || ''}`;
            } else if (toolDetails.response && toolDetails.response.reason) {
                detailsText = `Hours: 10:00 AM - 6:00 PM (Site Closed). Suggested: ${toolDetails.response.suggested_slots ? toolDetails.response.suggested_slots.join(', ') : 'Daytime Slots'}`;
            } else {
                detailsText = JSON.stringify(toolDetails.args || {});
            }

            toolCard.innerHTML = `
                <div class="tool-title">${isSuccess ? '✓ Site Visit Confirmed' : '⚠ Site Visit Unavailable'}</div>
                <div class="tool-detail">${detailsText}</div>
            `;
            bubble.appendChild(toolCard);
        }

        bubbleContainer.appendChild(bubble);

        // Add audio replay button for assistant turns
        if (role === 'assistant') {
            const btnPlay = document.createElement("button");
            btnPlay.className = "btn-speech-play";
            btnPlay.innerHTML = `<span>🔊</span> Listen`;
            btnPlay.addEventListener("click", () => speakText(content));
            bubbleContainer.appendChild(btnPlay);
        }

        group.appendChild(avatar);
        group.appendChild(bubbleContainer);

        chatViewport.appendChild(group);
        chatViewport.scrollTop = chatViewport.scrollHeight;
    }

    // Send user message to FastAPI backend, display typing animation, and render response
    async function sendMessage(messageText) {
        if (!messageText || !messageText.trim()) return;

        appendMessage('user', messageText);
        userInput.value = '';
        userInput.focus();

        typingIndicator.classList.remove("hidden");
        chatViewport.scrollTop = chatViewport.scrollHeight;
        btnSend.disabled = true;

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: messageText
                })
            });

            if (!response.ok) {
                throw new Error(`Server returned status: ${response.status}`);
            }

            const data = await response.json();
            typingIndicator.classList.add("hidden");

            appendMessage('assistant', data.response, data.tool_details);

            if (ttsToggle && ttsToggle.checked) {
                speakText(data.response);
            }

            if (analyticsBadgeCount) {
                analyticsBadgeCount.classList.remove("hidden");
            }

        } catch (error) {
            console.error("Chat error:", error);
            typingIndicator.classList.add("hidden");
            appendMessage('assistant', "I apologize, but our sales line is experiencing high traffic. Please allow me a moment or let me know how I can assist you with Northstar One.");
        } finally {
            btnSend.disabled = false;
        }
    }

    // Handle chat form submission
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (text) {
            sendMessage(text);
        }
    });

    // Event delegation handler for quick scenario buttons
    const scenarioScrollContainer = document.querySelector(".scenario-chips-scroll");
    if (scenarioScrollContainer) {
        scenarioScrollContainer.addEventListener("click", (e) => {
            const chip = e.target.closest("[data-msg]");
            if (chip) {
                const msg = chip.getAttribute("data-msg");
                if (msg) {
                    sendMessage(msg);
                }
            }
        });
    }

    // Microphone speech recognition setup (STT)
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';

        btnMic.addEventListener("click", () => {
            btnMic.style.background = "#fee2e2";
            btnMic.style.color = "#b91c1c";
            btnMic.style.borderColor = "#ef4444";
            recognition.start();
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            btnMic.style.background = "";
            btnMic.style.color = "";
            btnMic.style.borderColor = "";
            sendMessage(transcript);
        };

        recognition.onerror = (e) => {
            console.error("Speech recognition error:", e);
            btnMic.style.background = "";
            btnMic.style.color = "";
            btnMic.style.borderColor = "";
        };

        recognition.onend = () => {
            btnMic.style.background = "";
            btnMic.style.color = "";
            btnMic.style.borderColor = "";
        };
    } else {
        btnMic.title = "Speech recognition is not supported in this browser";
        btnMic.style.opacity = "0.5";
    }

    // Fetch and render CRM lead intelligence from backend
    btnGenerateAnalytics.addEventListener("click", async () => {
        btnGenerateAnalytics.disabled = true;
        btnGenerateAnalytics.innerHTML = `<span>⏳</span> Extracting Insights...`;

        try {
            const response = await fetch("/api/analytics", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId })
            });

            if (!response.ok) {
                throw new Error(`Analytics extraction failed: ${response.status}`);
            }

            const data = await response.json();
            renderAnalytics(data);

        } catch (error) {
            console.error("Analytics extraction error:", error);
            alert("Could not generate analytics. Please have at least one conversation turn with the advisor.");
        } finally {
            btnGenerateAnalytics.disabled = false;
            btnGenerateAnalytics.innerHTML = `
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <span>Extract Live Analytics</span>
            `;
        }
    });

    // Populate structured analytics metrics into drawer cards
    function renderAnalytics(data) {
        analyticsPlaceholder.classList.add("hidden");
        analyticsDetails.classList.remove("hidden");

        // Set interest badge style and text
        metricInterest.textContent = data.interest_level;
        metricInterest.className = "badge-status";
        if (data.interest_level === "High") metricInterest.classList.add("badge-high");
        else if (data.interest_level === "Medium") metricInterest.classList.add("badge-medium");
        else if (data.interest_level === "DND_Requested") metricInterest.classList.add("badge-dnd");
        else metricInterest.classList.add("badge-low");

        // Qualification details
        metricLanguage.textContent = data.language_detected;
        metricConfig.textContent = data.configuration_preference;
        metricBudget.textContent = data.budget_range;

        // Booking status
        metricSiteVisitStatus.textContent = data.site_visit_status;
        metricSiteVisitDetails.textContent = data.site_visit_details || (data.site_visit_status === 'Booked' ? 'Visit slot confirmed' : 'No visit scheduled');

        // Follow-up actions and customer sentiment
        metricFollowup.textContent = data.follow_up_requirement;
        metricCallbackTime.textContent = data.preferred_callback_time || 'None';
        metricSentiment.textContent = data.customer_sentiment;

        // Objections list
        metricObjectionsList.innerHTML = '';
        if (data.objections_raised && data.objections_raised.length > 0) {
            data.objections_raised.forEach(obj => {
                const li = document.createElement("li");
                li.textContent = obj;
                metricObjectionsList.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "None logged";
            metricObjectionsList.appendChild(li);
        }

        // Summary and recommended next action
        metricSummary.textContent = data.executive_summary;
        metricAction.textContent = data.recommended_next_action;

        // Raw structured JSON output
        rawJsonBlock.textContent = JSON.stringify(data, null, 2);
    }

    // Copy structured JSON payload to clipboard
    if (btnCopyJson) {
        btnCopyJson.addEventListener("click", () => {
            const jsonText = rawJsonBlock.textContent;
            if (jsonText) {
                navigator.clipboard.writeText(jsonText).then(() => {
                    const originalHtml = btnCopyJson.innerHTML;
                    btnCopyJson.innerHTML = `<span>✓</span> Copied!`;
                    setTimeout(() => { btnCopyJson.innerHTML = originalHtml; }, 2000);
                });
            }
        });
    }

    // Reset current conversation and initialize a fresh session
    btnNewSession.addEventListener("click", async () => {
        if (confirm("Start a new chat session? Current memory will be reset.")) {
            try {
                await fetch("/api/session/reset", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ session_id: sessionId })
                });
            } catch (e) {
                console.error("Reset error:", e);
            }

            sessionId = "sess_" + Math.random().toString(36).substring(2, 9);
            sessionStorage.setItem("northstar_session_id", sessionId);
            if (sessionDisplay) sessionDisplay.textContent = sessionId;

            // Reset chat viewport with initial greeting
            chatViewport.innerHTML = `
                <div class="message-group assistant-group">
                    <div class="avatar advisor-avatar">
                        <span>✦</span>
                    </div>
                    <div class="bubble-container">
                        <div class="bubble-meta">
                            <span class="sender-name">Northstar One AI Advisor</span>
                            <span class="message-time">Just now</span>
                        </div>
                        <div class="bubble assistant-bubble">
                            <p>Welcome to <strong>Northstar One</strong> by Northstar Homes. I am your Property Advisor for our luxury residential development in Sector 79, Gurugram.</p>
                            <p>We offer premium <strong>2 BHK (starting at ₹1.35 Cr)</strong> and <strong>3 BHK (starting at ₹1.75 Cr)</strong> residences with scenic Aravalli views and world-class amenities.</p>
                            <p>How can I assist you with your home search today?</p>
                        </div>
                    </div>
                </div>
            `;

            // Reset analytics drawer view
            analyticsPlaceholder.classList.remove("hidden");
            analyticsDetails.classList.add("hidden");
            rawJsonBlock.textContent = "";
            if (analyticsBadgeCount) analyticsBadgeCount.classList.add("hidden");
        }
    });
});
