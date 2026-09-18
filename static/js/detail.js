(() => {
    const hero = document.querySelector('.project-hero');
    if (!hero) return;

    const start = new Date(`${hero.dataset.start}T00:00:00`);
    const end = new Date(`${hero.dataset.end}T00:00:00`);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let percent = 0;
    let status = '未开始';
    let statusClass = 'is-pending';

    if (today >= end) {
        percent = 100;
        status = '已完成';
        statusClass = 'is-complete';
    } else if (today > start) {
        const duration = end - start;
        percent = duration > 0 ? Math.round(((today - start) / duration) * 100) : 100;
        status = '进行中';
        statusClass = '';
    }

    percent = Math.max(0, Math.min(100, percent));

    const statusBadge = document.querySelector('#projectStatus');
    statusBadge.textContent = status;
    if (statusClass) statusBadge.classList.add(statusClass);
    document.querySelector('#projectStatusText').textContent = status;
    document.querySelector('#projectProgressValue').textContent = `${percent}%`;
    document.querySelector('#projectProgressBar').style.width = `${percent}%`;
})();
