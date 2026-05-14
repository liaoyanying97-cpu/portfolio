// ========================================
// 滚动触发动画逻辑
// ========================================
function initScrollAnimations() {
    // 获取所有需要动画的元素
    const fadeElements = document.querySelectorAll('.fade-in');
    
    // 配置 Intersection Observer
    const observerOptions = {
        root: null, // 使用视口作为根
        rootMargin: '0px 0px -50px 0px', // 提前 50px 触发动画
        threshold: 0 // 只要元素边界进入视口就触发
    };
    
    // 创建 Observer
    const fadeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // 元素进入视口，添加动画类
                entry.target.classList.add('visible');
            } else {
                // 元素离开视口，移除动画类，确保下次进入时能再次触发
                entry.target.classList.remove('visible');
            }
        });
    }, observerOptions);
    
    // 开始观察每个元素
    fadeElements.forEach(el => {
        fadeObserver.observe(el);
    });
}

// 添加交互逻辑
document.addEventListener('DOMContentLoaded', () => {
    // 初始化滚动动画
    initScrollAnimations();

    // 获取所有的彩色文件夹（interactive-card）
    const interactiveCards = document.querySelectorAll('.interactive-card');

    interactiveCards.forEach(card => {
        card.addEventListener('click', () => {
            // 获取目标切图的 ID
            const targetId = card.getAttribute('data-target');
            if (targetId) {
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    // 平滑滚动到目标位置
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});