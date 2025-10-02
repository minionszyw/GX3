<template>
	<view class="container">
		<view class="stats-section">
			<view class="stats-header">
				<view class="stats-title">使用统计</view>
				<view class="stats-period">
					<picker mode="date" :value="endDate" fields="month" @change="onMonthChange">
						<view class="picker">
							{{ formatDate(endDate) }} ▼
						</view>
					</picker>
				</view>
			</view>
			
			<view class="stats-summary">
				<view class="summary-item">
					<view class="summary-label">总对话次数</view>
					<view class="summary-value">{{ stats.totalSessions }}</view>
				</view>
				
				<view class="summary-item">
					<view class="summary-label">总消耗Tokens</view>
					<view class="summary-value">{{ stats.totalTokens }}</view>
				</view>
				
				<view class="summary-item">
					<view class="summary-label">平均响应时间</view>
					<view class="summary-value">{{ stats.avgResponseTime }}ms</view>
				</view>
			</view>
		</view>
		
		<view class="chart-section">
			<view class="chart-title">每日使用情况</view>
			<view class="chart-container">
				<!-- 这里可以集成图表组件，如uCharts -->
				<view class="chart-placeholder">
					<image src="/static/chart-placeholder.png" mode="aspectFit" class="chart-image"></image>
					<view class="chart-text">使用统计图表</view>
				</view>
			</view>
		</view>
		
		<view class="details-section">
			<view class="details-title">详细记录</view>
			<view class="details-list">
				<view 
					v-for="record in usageRecords" 
					:key="record.id" 
					class="record-item"
				>
					<view class="record-info">
						<view class="record-date">{{ formatDateTime(record.date) }}</view>
						<view class="record-sessions">{{ record.sessions }}次对话</view>
					</view>
					<view class="record-tokens">{{ record.tokens }} tokens</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			endDate: new Date().toISOString().slice(0, 7), // 当前月份
			stats: {
				totalSessions: 25,
				totalTokens: 1250,
				avgResponseTime: 850
			},
			usageRecords: [
				{ id: 1, date: '2025-10-01', sessions: 3, tokens: 150 },
				{ id: 2, date: '2025-10-02', sessions: 2, tokens: 100 },
				{ id: 3, date: '2025-10-03', sessions: 5, tokens: 250 },
				{ id: 4, date: '2025-10-04', sessions: 1, tokens: 50 },
				{ id: 5, date: '2025-10-05', sessions: 4, tokens: 200 }
			]
		}
	},
	
	methods: {
		onMonthChange(e) {
			this.endDate = e.detail.value
			// 这里可以重新加载该月份的统计数据
			this.loadStats()
		},
		
		async loadStats() {
			// 模拟加载统计数据
			// 实际项目中这里会调用API获取统计数据
		},
		
		formatDate(dateString) {
			const date = new Date(dateString)
			return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' })
		},
		
		formatDateTime(dateString) {
			const date = new Date(dateString)
			return date.toLocaleDateString('zh-CN')
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

.stats-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.stats-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 30rpx;
}

.stats-title {
	font-size: 32rpx;
	font-weight: bold;
}

.stats-period {
	font-size: 28rpx;
	color: #666;
}

.picker {
	padding: 10rpx 20rpx;
	background-color: #f0f0f0;
	border-radius: 8rpx;
}

.stats-summary {
	display: flex;
	justify-content: space-between;
}

.summary-item {
	text-align: center;
	flex: 1;
}

.summary-label {
	font-size: 24rpx;
	color: #666;
	margin-bottom: 10rpx;
}

.summary-value {
	font-size: 36rpx;
	font-weight: bold;
	color: #007AFF;
}

.chart-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.chart-title {
	font-size: 32rpx;
	font-weight: bold;
	margin-bottom: 30rpx;
}

.chart-container {
	height: 300rpx;
}

.chart-placeholder {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 100%;
}

.chart-image {
	width: 200rpx;
	height: 200rpx;
	margin-bottom: 20rpx;
}

.chart-text {
	font-size: 28rpx;
	color: #999;
}

.details-section {
	background-color: white;
	border-radius: 20rpx;
	padding: 30rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.details-title {
	font-size: 32rpx;
	font-weight: bold;
	margin-bottom: 30rpx;
}

.record-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f0f0f0;
}

.record-item:last-child {
	border-bottom: none;
}

.record-info {
	flex: 1;
}

.record-date {
	font-size: 28rpx;
	color: #333;
	margin-bottom: 5rpx;
}

.record-sessions {
	font-size: 24rpx;
	color: #999;
}

.record-tokens {
	font-size: 28rpx;
	font-weight: bold;
	color: #007AFF;
}
</style>