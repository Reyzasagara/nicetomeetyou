# Modern CV/Resume Portfolio Website 🚀

A professional, fully-responsive single-page portfolio website inspired by modern CV designs. Features smooth animations, interactive elements, and a clean, minimalist aesthetic perfect for showcasing your professional profile.

## ✨ Features

### Layout & Structure
- **Full-Height Sections**: Hero, About, Skills, Portfolio, Testimonials, Contact
- **Fixed Navigation**: Sticky header with smooth-scroll links
- **Responsive Grid**: Built with Flexbox and CSS Grid
- **Mobile-First Design**: Fully responsive across all devices

### Interactive Components
- **Hero Section**
  - Parallax background effect
  - Animated typewriter text effect
  - Call-to-action buttons with ripple effects
  - Smooth scroll indicator

- **Navigation**
  - Sticky navbar with scroll detection
  - Mobile hamburger menu
  - Active section highlighting
  - Smooth scrolling to sections

- **About Section**
  - Two-column layout with image and text
  - Hover effects on profile image
  - Animated counters for statistics
  - Professional info cards

- **Skills Section**
  - Animated progress bars
  - Scroll-triggered animations
  - Shimmer effects on skill bars
  - Dual-column responsive layout

- **Portfolio Section**
  - Filterable project grid (All, MES, IoT, Automotive)
  - Hover overlays with project details
  - Lightbox modal for image viewing
  - Smooth transitions and animations

- **Testimonials Section**
  - Carousel/slider with multiple testimonials
  - Previous/Next navigation buttons
  - Dot indicators for slide selection
  - Auto-play with pause on hover
  - Fade-in animations

- **Contact Section**
  - Form with real-time validation
  - Contact information cards
  - Social media links
  - Animated icons with hover effects
  - Success/error message display

### Visual Effects & Animations
- **Scroll Animations**: AOS (Animate On Scroll) library integration
- **Hover Effects**: Smooth transitions on buttons, images, and cards
- **Parallax Background**: Fixed attachment on hero section
- **Ripple Effects**: Button click animations
- **Counter Animations**: Number incrementing on scroll
- **Typewriter Effect**: Dynamic text animation in hero
- **Progress Bars**: Animated skill level indicators

### Design Elements
- **Color Scheme**: 
  - Primary: Blue (#007bff)
  - Accent: Orange (#ff6b35) and Green (#28a745)
  - Text: Dark (#212529) and Light Gray (#6c757d)
  - Backgrounds: White and Light Gray (#f8f9fa)
- **Typography**: Montserrat font family (300-800 weights)
- **Shadows**: Subtle layered shadows for depth
- **Rounded Corners**: Modern 10px border radius
- **Spacing**: Generous padding and margins

## 🛠️ Technologies Used

- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with CSS Grid, Flexbox, CSS Variables
- **JavaScript (ES6+)**: Interactive features and animations
- **jQuery 3.6.0**: DOM manipulation and event handling
- **AOS Library**: Scroll-triggered animations
- **Font Awesome 6.4.0**: Icon library
- **Google Fonts**: Montserrat typography

## 📁 File Structure

```
nicetomeetyou/
├── index.html          # Main HTML structure
├── styles.css          # Complete CSS styling
├── script.js           # Interactive JavaScript
├── README.md           # Documentation
├── images/             # Image assets
│   └── Profile.jpg     # Profile photo
└── resume.pdf          # Downloadable CV (optional)
```

## 🚀 Getting Started

### 1. Customize Your Content

**Update Personal Information** in `index.html`:
- Replace "REYZA AGUNG GUNAWAN" with your name
- Update job title and descriptions
- Change email, phone, location in contact section
- Update social media links (LinkedIn, GitHub, Twitter)

**Add Your Photo**:
- Replace `images/Profile.jpg` with your professional photo
- Recommended size: 400x500px for optimal display

**Customize Skills**:
- Edit skill names and percentages in the Skills section
- Adjust `data-progress` attributes to match your skill levels

**Update Portfolio Projects**:
- Replace project images with your own work
- Update project titles and descriptions
- Change filter categories if needed

**Modify Testimonials**:
- Add real testimonials from clients or colleagues
- Update client photos and information

### 2. Styling Customization

Edit CSS variables in `styles.css` to match your brand:

```css
:root {
    --primary-color: #007bff;     /* Your brand color */
    --accent-orange: #ff6b35;     /* Accent color */
    --text-dark: #212529;         /* Main text color */
    /* ... more variables */
}
```

### 3. Add Your Resume

- Create or export your resume as PDF
- Save it as `resume.pdf` in the root directory
- The download button in the hero section will link to it

### 4. Deploy to GitHub Pages

1. **Initialize Git** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Modern portfolio website"
   ```

2. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Select "Deploy from branch"
   - Choose `main` branch
   - Click Save

4. **Access Your Site**:
   - Visit `https://yourusername.github.io/your-repo/`
   - Site deploys in 2-5 minutes

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+ (full features)
- **Tablet**: 768px-1199px (adjusted layout)
- **Mobile**: Below 768px (stacked layout, hamburger menu)

## ⚡ Performance Optimizations

- **Lazy Loading**: Images load as they enter viewport
- **CSS Animations**: Hardware-accelerated transforms
- **Reduced Motion**: Respects user preferences
- **Optimized Assets**: Compressed images and minified code

## 🎨 Customization Tips

1. **Change Colors**: Update CSS variables in `:root`
2. **Modify Fonts**: Replace Google Fonts link in HTML
3. **Add Sections**: Follow existing section structure
4. **Change Animations**: Adjust AOS attributes or CSS transitions
5. **Update Icons**: Use Font Awesome icon library

## 🐛 Troubleshooting

- **Images not loading**: Check file paths and names (case-sensitive)
- **Animations not working**: Ensure AOS library is loaded
- **Mobile menu stuck**: Clear browser cache
- **Form not validating**: Check JavaScript console for errors

## 📄 License

This project is open-source. Feel free to fork, modify, and use for your own portfolio!

## 🤝 Credits

Design inspired by professional portfolio templates like RyanCV.
Built with modern web standards and best practices.

---

**Made with ❤️ by Reyza Agung Gunawan**
