<template>
  <div class="container">
    <h1>📊 Ask Your Table</h1>

    <!-- File Upload -->
    <form @submit.prevent="handleFileUpload">
      <input type="file" @change="onFileChange" accept=".csv,.xlsx,.json" />
      <button type="submit">Upload</button>
    </form>

    <div v-if="fileUploaded" class="success">✅ File uploaded successfully!</div>

    <!-- Question -->
    <form @submit.prevent="askQuestion" class="chatbox">
      <input v-model="question" placeholder="Ask a question..." />
      <button type="submit">Ask</button>
    </form>

    <!-- Response -->
    <div class="response" v-if="answer">
      <strong>LLM Response:</strong>
      <p>{{ answer }}</p>
    </div>
  </div>
</template>

<script setup>
	import { ref } from 'vue'
	import axios from 'axios'

	const file = ref(null)
	const question = ref('')
	const answer = ref('')
	const fileUploaded = ref(false)

	const onFileChange = (e) => {
		file.value = e.target.files[0]
	}

	const handleFileUpload = async () => {
		if (!file.value) return alert("Please select a file")

		const formData = new FormData()
		formData.append("file", file.value)

		try {
		await axios.post("http://localhost:8000/upload", formData)
		fileUploaded.value = true
		answer.value = ''
		} catch (err) {
		console.error(err)
		alert("Upload failed")
		}
	}

	const askQuestion = async () => {
		if (!question.value) return alert("Enter a question")

		const formData = new FormData()
		formData.append("question", question.value)

		try {
		const res = await axios.post("http://localhost:8000/ask", formData)
		answer.value = res.data.answer
		} catch (err) {
		console.error(err)
		alert("Failed to get answer")
		}
	}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 2rem;
  font-family: sans-serif;
}

input[type="file"],
input[type="text"],
button {
  margin-top: 1rem;
  display: block;
}

.chatbox {
  margin-top: 2rem;
}

.response {
  margin-top: 2rem;
  padding: 1rem;
  border: 1px solid #ccc;
}
</style>

