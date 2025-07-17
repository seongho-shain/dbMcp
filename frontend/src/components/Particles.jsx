import { useEffect, useRef } from 'react'

const Particles = ({ 
  count = 50, 
  size = 2, 
  speed = 0.5, 
  color = '#1e91d6',
  opacity = 0.6,
  className = ''
}) => {
  const canvasRef = useRef(null)
  const animationRef = useRef(null)
  const particlesRef = useRef([])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const particles = particlesRef.current

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Particle class
    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width
        this.y = Math.random() * canvas.height
        this.vx = (Math.random() - 0.5) * speed
        this.vy = (Math.random() - 0.5) * speed
        this.life = Math.random() * 100
        this.decay = Math.random() * 0.02 + 0.005
      }

      update() {
        this.x += this.vx
        this.y += this.vy
        this.life -= this.decay

        // Bounce off edges
        if (this.x < 0 || this.x > canvas.width) {
          this.vx *= -1
        }
        if (this.y < 0 || this.y > canvas.height) {
          this.vy *= -1
        }

        // Reset if life is over
        if (this.life <= 0) {
          this.x = Math.random() * canvas.width
          this.y = Math.random() * canvas.height
          this.life = Math.random() * 100
        }
      }

      draw() {
        ctx.save()
        ctx.globalAlpha = (this.life / 100) * opacity
        ctx.fillStyle = color
        ctx.beginPath()
        ctx.arc(this.x, this.y, size, 0, Math.PI * 2)
        ctx.fill()
        ctx.restore()
      }
    }

    // Initialize particles
    particles.length = 0
    for (let i = 0; i < count; i++) {
      particles.push(new Particle())
    }

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      particles.forEach(particle => {
        particle.update()
        particle.draw()
      })

      // Draw connections between nearby particles
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x
          const dy = particles[i].y - particles[j].y
          const distance = Math.sqrt(dx * dx + dy * dy)

          if (distance < 100) {
            ctx.save()
            ctx.globalAlpha = (1 - distance / 100) * opacity * 0.3
            ctx.strokeStyle = color
            ctx.lineWidth = 0.5
            ctx.beginPath()
            ctx.moveTo(particles[i].x, particles[i].y)
            ctx.lineTo(particles[j].x, particles[j].y)
            ctx.stroke()
            ctx.restore()
          }
        }
      }

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [count, size, speed, color, opacity])

  return (
    <canvas
      ref={canvasRef}
      className={`particles ${className}`}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: -1,
      }}
    />
  )
}

export default Particles