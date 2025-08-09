<template>
	<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
		<header class="bg-white shadow-sm border-b">
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
				<div class="flex items-center gap-3">
					<div class="p-2 bg-blue-600 rounded-lg text-6xl">
						<span class="material-symbols-outlined text-gray-900">search_insights</span>
					</div>
					<div>
						<h1 class="text-3xl font-bold text-gray-900">Insightly</h1>
						<p class="text-gray-600">Find insights through conversations</p>
					</div>
				</div>
			</div>
		</header>

		<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<div class="mb-12">
				<h2 class="text-2xl font-bold text-center mb-8 text-gray-900">Powerful Features to Unlock Your Data</h2>
				<div class="grid md:grid-cols-2 gap-6">
					<div class="bg-white rounded-lg border-2 hover:border-blue-300 transition-colors shadow-sm">
						<div class="p-6">
							<div class="flex items-center gap-3 mb-4">
								<div class="p-2 bg-green-100 rounded-lg text-3xl">
									<span class="material-symbols-outlined text-green-600">docs</span>
								</div>
								<h3 class="text-xl font-semibold text-gray-900">Ask Questions About Files</h3>
							</div>
							<p class="text-gray-600 text-base">
								Upload any document, spreadsheet, or data file and ask specific questions about its content. Get
								instant answers and insights from your data.
							</p>
						</div>
					</div>
					<div class="bg-white rounded-lg border-2 hover:border-blue-300 transition-colors shadow-sm">
						<div class="p-6">
							<div class="flex items-center gap-3 mb-4">
								<div class="p-2 bg-purple-100 rounded-lg text-3xl">
									<span class="material-symbols-outlined text-purple-600">analytics</span>
								</div>
								<h3 class="text-xl font-semibold text-gray-900">Generate Charts & Visualizations</h3>
							</div>
							<p class="text-gray-600 text-base">
								Transform your data into beautiful charts and graphs. Request specific visualizations to better
								understand patterns and trends in your data.
							</p>
						</div>
					</div>
				</div>
			</div>

			<div class="grid lg:grid-cols-2 gap-8">
				<div class="space-y-6">
					<div class="bg-white rounded-lg shadow-sm border">
						<div class="p-6 border-b">
							<h3 class="font-semibold text-gray-900 text-2xl flex items-center gap-2">
								<span class="material-symbols-outlined">upload</span>
								<p class="text-lg">Upload Your File</p>
							</h3>
							<p class="text-gray-600 text-sm mt-1">Upload a document, spreadsheet, or data file to get started</p>
						</div>
						<div class="p-6 space-y-4">
							<div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
								<input
									type="file"
									@change="handleFileUpload"
									class="hidden"
									ref="fileInput"
									accept=".pdf,.doc,.docx,.xls,.xlsx,.csv,.txt,.json"
								/>
								<div @click="$refs.fileInput.click()" class="cursor-pointer">
									<div class="text-xl">
										<span class="material-symbols-outlined text-gray-400 mx-auto mb-4">upload</span>
									</div>
									<p class="text-lg font-medium text-gray-700">Click to upload or drag and drop</p>
									<p class="text-sm text-gray-500 mt-2">PDF, DOC, XLS, CSV, TXT, JSON files supported</p>
								</div>
							</div>

							<div v-if="uploadedFile" class="bg-green-50 border border-green-200 rounded-lg p-4">
								<div class="flex items-center gap-3">
									<span class="material-symbols-outlined text-green-600">upload_file</span>
									<div>
										<p class="font-medium text-green-800">{{ uploadedFile.name }}</p>
										<p class="text-sm text-green-600">{{ (uploadedFile.size / 1024 / 1024).toFixed(2) }} MB</p>
									</div>
									<span class="ml-auto bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded">
										Uploaded
									</span>
								</div>
							</div>

							<div v-if="isUploading" class="flex items-center justify-center mt-4">
								<div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
								<span class="ml-2 text-blue-600">Uploading...</span>
							</div>
							<div v-if="uploadError" class="text-red-600 mt-2">{{ uploadError }}</div>

							<div v-if="filePreview" class="mt-4">
								<p class="text-sm font-medium text-gray-700 mb-2">Preview:</p>
								<div class="border rounded-lg overflow-hidden">
									<img
										:src="filePreview"
										alt="File preview"
										class="w-full h-48 object-cover"
									/>
								</div>
							</div>
						</div>
					</div>

					<div class="bg-white rounded-lg shadow-sm border">
						<div class="p-6 border-b">
							<h3 class="text-2xl font-semibold text-gray-900 flex items-center gap-2">
								<span class="material-symbols-outlined">send</span>
								<p class="text-lg">Ask Your Question</p>
							</h3>
							<p class="text-gray-600 text-sm mt-1">What would you like to know about your file?</p>
						</div>
						<div class="p-6 space-y-4">
							<textarea
								v-model="query"
								placeholder="e.g., 'What are the main trends in this data?' or 'Create a bar chart showing sales by region'"
								class="w-full min-h-[100px] px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
							></textarea>
							<button
								@click="handleSubmit"
								:disabled="!uploadedFile || !query.trim() || isLoading"
								class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-md transition-colors flex items-center justify-center gap-2"
							>
								<div v-if="isLoading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
								<span v-else class="material-symbols-outlined">send</span>
								{{ isLoading ? 'Processing...' : 'Get Insights' }}
							</button>
						</div>
					</div>
				</div>

				<div>
					<div class="bg-white rounded-lg shadow-sm border h-full">
						<div class="p-6 border-b">
							<h3 class="text-lg font-semibold text-gray-900">AI Response</h3>
							<p class="text-gray-600 text-sm mt-1">Your insights and visualizations will appear here</p>
						</div>
						<div class="p-6">
							<div v-if="isLoading" class="flex items-center justify-center h-64">
								<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
							</div>
							<div v-else-if="error" class="text-red-600 text-center py-8">
								{{ error }}
							</div>
							<div v-else-if="response" class="space-y-4">
								<!-- Text Response -->
								<div v-if="response.type === 'text'" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
									<p class="text-gray-800 leading-relaxed whitespace-pre-line">{{ response.answer }}</p>
								</div>
								<!-- Chart Response -->
								<div v-else-if="response.type === 'chart'" class="flex flex-col items-center space-y-2">
									<img
										:src="'data:image/png;base64,' + response.chart"
										alt="Chart"
										class="max-w-full rounded-lg border"
									/>
									<p v-if="response.description" class="text-gray-700 text-sm text-center">{{ response.description }}</p>
								</div>
							</div>
							<div v-else class="flex flex-col items-center justify-center h-64 text-gray-500">
								<div class="text-4xl">
									<span class="material-symbols-outlined mb-4 text-gray-300">tab_search</span>
								</div>
								<p class="text-lg font-medium">Upload a file and ask a question</p>
								<p class="text-sm text-center mt-2">Your AI-powered insights will appear here</p>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="mt-12">
				<h3 class="text-lg font-semibold mb-4 text-gray-900">Example Questions You Can Ask:</h3>
				<div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
					<button
						v-for="(example, index) in exampleQueries"
						:key="index"
						@click="query = example"
						class="text-left justify-start h-auto p-3 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 hover:border-gray-400 transition-colors"
					>
						"{{ example }}"
					</button>
				</div>
			</div>
		</main>
	</div>
</template>

<script setup>
	import { ref } from 'vue'
	import axios from 'axios'

	//import sampleChart from '../samplechart.json'
	//import sampleText from '../sampletext.json'

	const uploadedFile = ref(null)
	const filePreview = ref(null)
	const query = ref('')
	const response = ref(null)
	const isLoading = ref(false)
	const error = ref(null)
	const isUploading = ref(false)
	const uploadError = ref(null)

	const exampleQueries = [
		'What are the key insights from this data?',
		'Create a line chart between the related columns',
		'Show me trends over time',
		'What patterns do you see?',
		'Generate a summary report',
		'Compare different segments'
	]

	const handleFileUpload = async (event) => {
		const file = event.target.files?.[0]
		if (file) {
			uploadedFile.value = null
			uploadError.value = null
			isUploading.value = true

			if (file.type.startsWith('image/')) {
				const reader = new FileReader()
				reader.onload = (e) => {
					filePreview.value = e.target?.result
				}
				reader.readAsDataURL(file)
			} else {
				filePreview.value = null
			}
			const formData = new FormData()
			formData.append("file", file)
			try {
				await axios.post("http://localhost:8000/upload", formData)
				uploadedFile.value = file
			} catch (err) {
				console.error(err)
				uploadError.value = "Failed to upload file"
				uploadedFile.value = null
			} finally {
				isUploading.value = false
			}
		}
	}

	const handleSubmit = async () => {
		if (!uploadedFile.value || !query.value.trim()) return
		isLoading.value = true
		error.value = null
		response.value = null
		try {
			// const formData = new FormData()
			// formData.append("question", query.value)
			// const res = await axios.post("http://localhost:8000/ask", formData)
			// response.value = res.data
			if (query.value.toLowerCase().includes('chart')) {
				response.value = sampleChart
			} else {
				response.value = sampleText
			}
			throw new Error("Unexpected query format")
		} catch (err) {
			console.error(err)
			error.value = "Failed to get answer"
		} finally {
			isLoading.value = false
		}
	}
</script>