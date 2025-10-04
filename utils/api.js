// API工具函数
const API_BASE_URL = 'http://localhost:8000/api'

class ApiClient {
	constructor() {
		this.baseUrl = API_BASE_URL
	}
	
	// 获取认证token
	getAuthToken() {
		try {
			return uni.getStorageSync('token')
		} catch (error) {
			console.error('获取token失败:', error)
			return null
		}
	}
	
	// 通用请求方法
	async request(url, options = {}) {
		const token = this.getAuthToken()
		const defaultOptions = {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				...options.headers
			}
		}
		
		// 如果有token，添加到请求头
		if (token) {
			defaultOptions.headers['Authorization'] = `Bearer ${token}`
		}
		
		const config = {
			...defaultOptions,
			...options
		}
		
		// 构造完整URL
		const fullUrl = url.startsWith('http') ? url : `${this.baseUrl}${url}`
		
		return new Promise((resolve, reject) => {
			uni.request({
				url: fullUrl,
				method: config.method,
				header: config.headers,
				data: config.body ? JSON.parse(config.body) : config.data,
				success: (res) => {
					if (res.statusCode >= 200 && res.statusCode < 300) {
						resolve(res.data)
					} else {
						reject(new Error(`请求失败: ${res.statusCode}`))
					}
				},
				fail: (err) => {
					reject(new Error(`网络错误: ${err.errMsg}`))
				}
			})
		})
	}
	
	// GET请求
	get(url, options = {}) {
		return this.request(url, { ...options, method: 'GET' })
	}
	
	// POST请求
	post(url, data, options = {}) {
		return this.request(url, { 
			...options, 
			method: 'POST', 
			body: JSON.stringify(data) 
		})
	}
	
	// PUT请求
	put(url, data, options = {}) {
		return this.request(url, { 
			...options, 
			method: 'PUT', 
			body: JSON.stringify(data) 
		})
	}
	
	// DELETE请求
	delete(url, options = {}) {
		return this.request(url, { ...options, method: 'DELETE' })
	}
}

// 创建API客户端实例
const apiClient = new ApiClient()

// 导出API客户端实例和请求方法
export default apiClient
export { ApiClient }