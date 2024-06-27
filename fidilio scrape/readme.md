# توضیحات این پوشه
به پیشنهاد آقای امیرعلی رستگاری این [لینک](https://fidilio.com/map) رو چک کردم و به api سایت fidilito دسترسی پیدا کردیم.
 اطلاعات کل رستوران‌ها داخل فایل‌های [‍‍```MenuCategory.csv```](/fidilio%20scrape/MenuCategory.csv) ، ‍‍[‍```MenuItem.csv```](/fidilio%20scrape/saat_kari.csv) ، [‍```saat_kari.csv```](/fidilio%20scrape/MenuItem.csv) و [‍```telephone.csv```](/fidilio%20scrape/telephone.csv) ذخیره می‌شه.

# کارهایی که باید انجام بشه
- [x] تمیز کردن ستون ```types``` و ```styles``` از دیتا فریم موجود که در فایل [```scrape.py```](/fidilio%20scrape/scrape.py) اسخراج می‌شود.
- [x] استخراج منوی فروشگاه‌هایی که شناسایی شدن.
- [ ] استخراج ساعت کاری‌ها.

# هشدار خطای آدرس دهی
این کدها مبتنی بر لینوکس نوشته شده داخل ویندوز آدرس دهی‌ها به صورت
```path\\dir``` است ولی در ویندوز ```path/dir``` لطفا این بخش‌ها را به صورت دستی تغییر دهید تا کدتان با خطا مواجه نشود.