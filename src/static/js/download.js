async function downloadFile(fileId) {
    try {
        // Отправляем запрос на сервер для скачивания файла
        const response = await fetch(`/files/download/${fileId}`, {
            method: "GET",
            headers: {
                "Accept": "application/json",  // Принять файл как json
            },
        });

        if (response.ok) {
            // Получаем имя файла из заголовка Content-Disposition
            const contentDisposition = response.headers.get("Content-Disposition");
            const filenameMatch = contentDisposition.match(/filename\*=utf-8''(.+)/);
            const filename = filenameMatch ? decodeURIComponent(filenameMatch[1]) : `file_${fileId}`;

            const blob = await response.blob();  // Получаем файл как Blob
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = filename;  // Используем имя из заголовка
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);  // Очищаем URL

            // Обновляем количество скачиваний на странице
            const downloadsElement = document.getElementById(`downloads-${fileId}`);
            if (downloadsElement) {
                let currentDownloads = parseInt(downloadsElement.textContent, 10);
                downloadsElement.textContent = `${currentDownloads + 1}`; // Увеличиваем на 1
            }
        } else {
            alert("Error downloading the file.");
        }
    } catch (error) {
        console.error("Error during file download:", error);
        alert("Error downloading the file.");
    }
}
