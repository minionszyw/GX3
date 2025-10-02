import { defineStore } from 'pinia'
import apiClient from '@/utils/api'

export const useBillingStore = defineStore('billing', {
	state: () => ({
		balance: 1000, // 用户余额，单位为tokens
		transactions: [], // 交易记录
		isLoading: false, // 加载状态
		error: null // 错误信息
	}),
	
	actions: {
		// 获取用户余额
		async fetchBalance() {
			try {
				this.isLoading = true
				const response = await apiClient.get('/user/balance')
				this.balance = response.balance
				return response
			} catch (error) {
				this.error = error.message
				throw error
			} finally {
				this.isLoading = false
			}
		},
		
		// 充值tokens
		async rechargeTokens(amount) {
			try {
				this.isLoading = true
				const response = await apiClient.post('/billing/recharge', {
					amount: amount
				})
				
				// 更新本地余额
				this.balance = response.balance
				return response
			} catch (error) {
				this.error = error.message
				throw error
			} finally {
				this.isLoading = false
			}
		},
		
		// 获取交易记录
		async fetchTransactions() {
			try {
				this.isLoading = true
				const response = await apiClient.get('/billing/transactions')
				this.transactions = response.transactions
				return response
			} catch (error) {
				this.error = error.message
				throw error
			} finally {
				this.isLoading = false
			}
		},
		
		// 消费tokens
		async consumeTokens(amount, description = '') {
			try {
				this.isLoading = true
				const response = await apiClient.post('/billing/consume', {
					amount: amount,
					description: description
				})
				
				// 更新本地余额
				this.balance = response.balance
				return response
			} catch (error) {
				this.error = error.message
				throw error
			} finally {
				this.isLoading = false
			}
		},
		
		// 格式化token显示
		formatTokens(tokens) {
			// 100 tokens = 1元
			return (tokens / 100).toFixed(2)
		}
	},
	
	getters: {
		// 余额格式化显示
		formattedBalance: (state) => {
			return (state.balance / 100).toFixed(2)
		},
		
		// 余额是否充足
		hasSufficientBalance: (state) => (amount) => {
			return state.balance >= amount
		}
	}
})