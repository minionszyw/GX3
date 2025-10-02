<template>
	<view class="container">
		<view class="form-section">
			<view class="form-item">
				<label class="form-label">头像</label>
				<view class="avatar-upload">
					<image class="avatar-preview" :src="userInfo.avatar || '/static/default-avatar.png'" mode="aspectFill"></image>
					<button class="upload-btn" @click="uploadAvatar">上传头像</button>
				</view>
			</view>
			
			<view class="form-item">
				<label class="form-label">昵称</label>
				<input class="form-input" v-model="form.nickname" placeholder="请输入昵称" />
			</view>
			
			<view class="form-item">
				<label class="form-label">邮箱</label>
				<input class="form-input" v-model="form.email" placeholder="请输入邮箱" type="email" />
			</view>
			
			<button class="save-btn" @click="saveProfile">保存</button>
		</view>
	</view>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useUserStore } from '@/store/user/user'

export default {
	data() {
		return {
			form: {
				nickname: '',
				email: '',
				avatar: ''
			}
		}
	},
	
	computed: {
		...mapState(useUserStore, ['userInfo'])
	},
	
	onLoad() {
		// 初始化表单数据
		this.form.nickname = this.userInfo.nickname
		this.form.email = this.userInfo.email
		this.form.avatar = this.userInfo.avatar
	},
	
	methods: {
		...mapActions(useUserStore, ['updateUserInfo']),
		
		uploadAvatar() {
			// 选择图片
			uni.chooseImage({
				count: 1,
				success: (res) => {
					// 模拟上传头像
					uni.showToast({
						title: '头像上传成功',
						icon: 'success'
					})
					this.form.avatar = res.tempFilePaths[0]
				}
			})
		},
		
		async saveProfile() {
			try {
				const updatedInfo = {
					nickname: this.form.nickname,
					email: this.form.email,
					avatar: this.form.avatar
				}
				
				await this.updateUserInfo(updatedInfo)
				
				uni.showToast({
					title: '保存成功',
					icon: 'success'
				})
				
				// 返回上一页
				setTimeout(() => {
					uni.navigateBack()
				}, 1000)
			} catch (error) {
				uni.showToast({
					title: '保存失败',
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

.form-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 30rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.form-item {
	margin-bottom: 30rpx;
}

.form-label {
	display: block;
	font-size: 28rpx;
	color: #333;
	margin-bottom: 15rpx;
}

.form-input {
	width: 100%;
	padding: 20rpx;
	border: 1rpx solid #eee;
	border-radius: 10rpx;
	font-size: 28rpx;
	box-sizing: border-box;
}

.avatar-upload {
	display: flex;
	align-items: center;
}

.avatar-preview {
	width: 120rpx;
	height: 120rpx;
	border-radius: 50%;
	margin-right: 30rpx;
}

.upload-btn {
	font-size: 24rpx;
	padding: 15rpx 30rpx;
	background-color: #f0f0f0;
	border: none;
	border-radius: 8rpx;
}

.save-btn {
	width: 100%;
	background-color: #007AFF;
	color: white;
	border: none;
	padding: 25rpx;
	border-radius: 10rpx;
	font-size: 32rpx;
	margin-top: 30rpx;
}
</style>