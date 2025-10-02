import { defineStore } from 'pinia'
import apiClient from '@/utils/api'

export const useUserStore = defineStore('user', {
	state: () => ({
		userInfo: {
			id: null,
			nickname: '',
			avatar: '',
			tokens: 1000, // 新用户默认1000 tokens（相当于10元）
			email: '',
			openid: ''
		}, // 用户信息
		token: '', // JWT token
		isLoggedIn: false, // 登录状态
		error: null // 错误信息
	}),
	
	actions: {
		// 微信登录
		async loginWithWechat() {
			try {
				// 实际微信登录API调用
				const response = await apiClient.post('/auth/wechat-login')
				
				this.token = response.token
				this.userInfo = response.user
				this.isLoggedIn = true
				
				// 保存token到本地存储
				uni.setStorageSync('token', this.token)
				uni.setStorageSync('userInfo', this.userInfo)
				
				return response
			} catch (error) {
				this.error = error.message
				throw error
			}
		},
		
		// 邮箱登录
		async loginWithEmail(credentials) {
			try {
				// 实际邮箱登录API调用
				const response = await apiClient.post('/auth/email-login', credentials)
				
				this.token = response.token
				this.userInfo = response.user
				this.isLoggedIn = true
				
				// 保存token到本地存储
				uni.setStorageSync('token', this.token)
				uni.setStorageSync('userInfo', this.userInfo)
				
				return response
			} catch (error) {
				this.error = error.message
				throw error
			}
		},
		
		// 退出登录
		logout() {
			// 清除登录状态
			this.token = ''
			this.userInfo = {
				id: null,
				nickname: '',
				avatar: '',
				tokens: 1000,
				email: '',
				openid: ''
			}
			this.isLoggedIn = false
			
			// 清除本地存储的token
			uni.removeStorageSync('token')
			uni.removeStorageSync('userInfo')
		},
		
		// 检查登录状态
		checkAuthStatus() {
			const token = uni.getStorageSync('token')
			const userInfo = uni.getStorageSync('userInfo')
			
			if (token && userInfo) {
				this.token = token
				this.userInfo = userInfo
				this.isLoggedIn = true
				// 这里可以添加token有效性验证逻辑
				return true
			}
			
			return false
		},
		
		// 更新用户信息
		async updateUserInfo(userInfo) {
			try {
				// 实际API调用
				const response = await apiClient.put('/user/profile', userInfo)
				
				this.userInfo = response
				// 更新本地存储
				uni.setStorageSync('userInfo', this.userInfo)
				
				return response
			} catch (error) {
				this.error = error.message
				throw error
			}
		},
		
		// 充值token
		async rechargeTokens(amount) {
			try {
				// 实际充值API调用
				const response = await apiClient.post('/billing/recharge', {
					amount: amount
				})
				
				this.userInfo.tokens = response.tokens
				// 更新本地存储
				uni.setStorageSync('userInfo', this.userInfo)
				
				return response
			} catch (error) {
				this.error = error.message
				throw error
			}
		}
	}
})