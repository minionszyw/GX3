<template>
	<view class="container">
		<view class="balance-section">
			<view class="balance-label">当前余额</view>
			<view class="balance-amount">¥{{ (userInfo.tokens / 100).toFixed(2) }}</view>
		</view>
		
		<view class="recharge-options">
			<view class="option-title">充值金额</view>
			
			<view class="amount-options">
				<view 
					v-for="amount in rechargeAmounts" 
					:key="amount.value" 
					class="amount-item" 
					:class="{ active: selectedAmount === amount.value }"
					@click="selectAmount(amount.value)"
				>
					<view class="amount-price">¥{{ amount.price }}</view>
					<view class="amount-tokens">{{ amount.tokens }} tokens</view>
				</view>
			</view>
			
			<view class="custom-amount">
				<view class="custom-label">自定义金额</view>
				<input 
					class="custom-input" 
					v-model="customAmount" 
					placeholder="请输入充值金额" 
					type="digit" 
					@blur="handleCustomAmount"
				/>
			</view>
			
			<button class="recharge-btn" @click="confirmRecharge" :disabled="!selectedAmount">立即充值</button>
		</view>
		
		<view class="recharge-rules">
			<view class="rules-title">充值说明</view>
			<view class="rule-item">• 1元 = 100 tokens</view>
			<view class="rule-item">• 充值金额不可退款</view>
			<view class="rule-item">• tokens永久有效</view>
		</view>
	</view>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useUserStore } from '@/store/user/user'

export default {
	data() {
		return {
			selectedAmount: 0,
			customAmount: '',
			rechargeAmounts: [
				{ price: 10, tokens: 1000 },
				{ price: 30, tokens: 3000 },
				{ price: 50, tokens: 5000 },
				{ price: 100, tokens: 10000 }
			]
		}
	},
	
	computed: {
		...mapState(useUserStore, ['userInfo'])
	},
	
	methods: {
		...mapActions(useUserStore, ['rechargeTokens']),
		
		selectAmount(amount) {
			this.selectedAmount = amount
			this.customAmount = ''
		},
		
		handleCustomAmount() {
			if (this.customAmount) {
				const amount = parseFloat(this.customAmount)
				if (!isNaN(amount) && amount > 0) {
					this.selectedAmount = amount * 100 // 转换为tokens
				} else {
					this.customAmount = ''
				}
			}
		},
		
		async confirmRecharge() {
			if (!this.selectedAmount) return
			
			uni.showModal({
				title: '确认充值',
				content: `确定要充值¥${(this.selectedAmount / 100).toFixed(2)}吗？`,
				success: async (res) => {
					if (res.confirm) {
						try {
							// 模拟支付流程
							await this.simulatePayment()
							
							// 更新用户token余额
							await this.rechargeTokens(this.selectedAmount)
							
							uni.showToast({
								title: '充值成功',
								icon: 'success'
							})
							
							// 返回个人中心页面
							setTimeout(() => {
								uni.navigateBack()
							}, 1500)
						} catch (error) {
							uni.showToast({
								title: '充值失败',
								icon: 'none'
							})
						}
					}
				}
			})
		},
		
		async simulatePayment() {
			// 模拟支付过程
			return new Promise((resolve) => {
				setTimeout(() => {
					resolve()
				}, 1500)
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.container {
	background-color: #f5f5f5;
	min-height: 100vh;
	padding: 20rpx;
}

.balance-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 40rpx;
	text-align: center;
	margin-bottom: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.balance-label {
	font-size: 28rpx;
	color: #666;
	margin-bottom: 20rpx;
}

.balance-amount {
	font-size: 48rpx;
	font-weight: bold;
	color: #007AFF;
}

.recharge-options {
	background-color: white;
	border-radius: 20rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.option-title {
	font-size: 32rpx;
	font-weight: bold;
	margin-bottom: 30rpx;
}

.amount-options {
	display: flex;
	flex-wrap: wrap;
	justify-content: space-between;
	margin-bottom: 30rpx;
}

.amount-item {
	width: 48%;
	background-color: #f8f8f8;
	border-radius: 15rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;
	text-align: center;
}

.amount-item.active {
	background-color: #e6f2ff;
	border: 1rpx solid #007AFF;
}

.amount-price {
	font-size: 36rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 10rpx;
}

.amount-tokens {
	font-size: 24rpx;
	color: #666;
}

.custom-amount {
	margin-bottom: 30rpx;
}

.custom-label {
	font-size: 28rpx;
	color: #333;
	margin-bottom: 15rpx;
}

.custom-input {
	width: 100%;
	padding: 20rpx;
	border: 1rpx solid #eee;
	border-radius: 10rpx;
	font-size: 28rpx;
	box-sizing: border-box;
}

.recharge-btn {
	width: 100%;
	background-color: #007AFF;
	color: white;
	border: none;
	padding: 25rpx;
	border-radius: 10rpx;
	font-size: 32rpx;
}

.recharge-btn:disabled {
	background-color: #ccc;
}

.recharge-rules {
	background-color: white;
	border-radius: 20rpx;
	padding: 30rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.rules-title {
	font-size: 32rpx;
	font-weight: bold;
	margin-bottom: 20rpx;
}

.rule-item {
	font-size: 24rpx;
	color: #666;
	margin-bottom: 10rpx;
}
</style>