// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Dummy course-related conversation
    appendMessage('Alice: Hey, have you taken any interesting courses lately?');
    appendMessage('Bob: Yes, I just finished a great machine learning course.');
    appendMessage('Charlie: That sounds awesome! Can you recommend it?');
    appendMessage('Charlie: I took a comprehensive data science course last semester. It covered everything from statistics to machine learning.');
    appendMessage('Alice: That sounds perfect for Eve! What was the course name, Charlie?');
    appendMessage('Charlie: It was called "Data Science Essentials." I Highly recommended It!');
    appendMessage('Alice:Im super passionate about this stuff');
  });
  
  function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();
  
    if (message !== '') {
      appendMessage('You: ' + message);
      // You can send the message to the server here
      // Example: socket.emit('message', { user: 'You', text: message });
      messageInput.value = '';
    }
  }
  
  function appendMessage(message) {
    var chatWindow = document.getElementById('chat-window');
    var newMessage = document.createElement('div');
    newMessage.textContent = message;
    chatWindow.appendChild(newMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
  