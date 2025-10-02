<template>
	<view class="container">
		<view class="header">
			<navigator class="back-btn" open-type="navigateBack">←</navigator>
			<view class="title">注册账号</view>
		</view>
		
		<view class="register-form">
			<view class="form-item">
				<input 
					class="form-input" 
					v-model="form.email" 
					placeholder="请输入邮箱" 
					type="email" 
					@confirm="register"
				/>
			</view>
			
			<view class="form-item">
				<input 
					class="form-input" 
					v-model="form.nickname" 
					placeholder="请输入昵称" 
					@confirm="register"
				/>
			</view>
			
			<view class="form-item">
				<input 
					class="form-input" 
					v-model="form.password" 
					placeholder="请输入密码" 
					type="password" 
					@confirm="register"
				/>
			</view>
			
			<view class="form-item">
				<input 
					class="form-input" 
					v-model="form.confirmPassword" 
					placeholder="请再次输入密码" 
					type="password" 
					@confirm="register"
				/>
			</view>
			
			<view class="form-item">
				<view class="verification">
					<input 
						class="code-input" 
						v-model="form.verificationCode" 
						placeholder="请输入验证码" 
						@confirm="register"
					/>
					<button 
						class="code-btn" 
						@click="sendVerificationCode" 
						:disabled="codeCountdown > 0"
					>
						{{ codeCountdown > 0 ? `${codeCountdown}秒后重发` : '发送验证码' }}
					</button>
				</view>
			</view>
			
			<button class="register-btn" @click="register" :disabled="!canRegister">注册</button>
			
			<view class="agreement">
				注册即表示您同意
				<navigator class="link" url="/pages/auth/agreement">用户协议</navigator>
				和
				<navigator class="link" url="/pages/auth/privacy">隐私政策</navigator>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			form: {
				email: '',
				nickname: '',
				password: '',
				confirmPassword: '',
				verificationCode: ''
			},
			codeCountdown: 0
		}
	},
	
	computed: {
		canRegister() {
			return this.form.email && 
				   this.form.nickname && 
				   this.form.password && 
				   this.form.confirmPassword && 
				   this.form.verificationCode &&
				   this.form.password === this.form.confirmPassword
		}
	},
	
	methods: {
		async sendVerificationCode() {
			if (!this.form.email) {
				uni.showToast({
					title: '请输入邮箱',
					icon: 'none'
				})
				return
			}
			
			// 模拟发送验证码
			try {
				// 这里调用发送验证码的API
				await new Promise(resolve => {
					setTimeout(() => {
						resolve()
					}, 1000)
				})
				
				uni.showToast({
					title: '验证码已发送',
					icon: 'success'
				})
				
				// 开始倒计时
				this.startCountdown()
			} catch (error) {
				uni.showToast({
					title: '发送失败，请重试',
					icon: 'none'
				})
			}
		},
		
		startCountdown() {
			this.codeCountdown = 60
			const timer = setInterval(() => {
				this.codeCountdown--
				if (this.codeCountdown <= 0) {
					clearInterval(timer)
				}
			}, 1000)
		},
		
		async register() {
			if (!this.canRegister) {
				if (this.form.password !== this.form.confirmPassword) {
					uni.showToast({
						title: '两次密码输入不一致',
						icon: 'none'
					})
				} else {
					uni.showToast({
						title: '请完善所有信息',
						icon: 'none'
					})
				}
				return
			}
			
			// 模拟注册过程
			try {
				// 这里调用注册API
				await new Promise(resolve => {
					setTimeout(() => {
						resolve()
					}, 1500)
				})
				
				uni.showToast({
					title: '注册成功',
					icon: 'success'
				})
				
				// 注册成功后跳转到登录页面
				setTimeout(() => {
					uni.redirectTo({
						url: '/pages/auth/login'
					})
				}, 1500)
			} catch (error) {
				uni.showToast({
					title: '注册失败，请重试',
					icon: 'none'
				})
			}
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

.header {
	display: flex;
	align-items: center;
	padding: 20rpx 0;
	margin-bottom: 40rpx;
}

.back-btn {
	font-size: 36rpx;
	color: #333;
	padding: 20rpx;
}

.title {
	flex: 1;
	text-align: center;
	font-size: 36rpx;
	font-weight: bold;
	color: #333;
}

.register-form {
	background-color: white;
	border-radius: 20rpx;
	padding: 40rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.form-item {
	margin-bottom: 30rpx;
}

.form-input {
	width: 100%;
	padding: 25rpx;
	border: 1rpx solid #eee;
	border-radius: 10rpx;
	font-size: 28rpx;
	box-sizing: border-box;
}

.verification {
	display: flex;
}

.code-input {
	flex: 1;
	padding: 25rpx;
	border: 1rpx solid #eee;
	border-radius: 10rpx 0 0 10rpx;
	font-size: 28rpx;
	box-sizing: border-box;
}

.code-btn {
	white-space: nowrap;
	padding: 25rpx 30rpx;
	background-color: #007AFF;
	color: white;
	border: none;
	border-radius: 0 10rpx 10rpx 0;
	font-size: 28rpx;
}

.code-btn:disabled {
	background-color: #ccc;
}

.register-btn {
	width: 100%;
	background-color: #007AFF;
	color: white;
	border: none;
	padding: 25rpx;
	border-radius: 10rpx;
	font-size: 32rpx;
	margin-top: 20rpx;
}

.register-btn:disabled {
	background-color: #ccc;
}

.agreement {
	text-align: center;
	font-size: 24rpx;
	color: #999;
	margin-top: 30rpx;
	line-height: 1.5;
}

.link {
	color: #007AFF;
	display: inline;
}

.link:hover {
	text-decoration: underline;
}
</style>