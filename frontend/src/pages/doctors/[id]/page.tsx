"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { Plus, Mail, Phone, ArrowLeft, X, Stethoscope } from "lucide-react"

interface Doctor {
  id: number
  name: string
  email: string
  phone: string
  specialization: string
  image?: string
}

const MOCK_DOCTORS: Doctor[] = [
  {
    id: 1,
    name: "Dr. Sarah Johnson",
    email: "sarah.johnson@hospital.com",
    phone: "+1 (555) 123-4567",
    specialization: "Cardiology",
    image: "/doctor-placeholder.svg",
  },
  {
    id: 2,
    name: "Dr. Michael Chen",
    email: "michael.chen@hospital.com",
    phone: "+1 (555) 234-5678",
    specialization: "Neurology",
    image: "/doctor-placeholder.svg",
  },
  {
    id: 3,
    name: "Dr. Emily Rodriguez",
    email: "emily.rodriguez@hospital.com",
    phone: "+1 (555) 345-6789",
    specialization: "Pediatrics",
    image: "/doctor-placeholder.svg",
  },
  {
    id: 4,
    name: "Dr. James Wilson",
    email: "james.wilson@hospital.com",
    phone: "+1 (555) 456-7890",
    specialization: "Orthopedics",
    image: "/doctor-placeholder.svg",
  },
  {
    id: 5,
    name: "Dr. Priya Patel",
    email: "priya.patel@hospital.com",
    phone: "+1 (555) 567-8901",
    specialization: "Dermatology",
    image: "/doctor-placeholder.svg",
  },
  {
    id: 6,
    name: "Dr. Robert Martinez",
    email: "robert.martinez@hospital.com",
    phone: "+1 (555) 678-9012",
    specialization: "General Surgery",
    image: "/doctor-placeholder.svg",
  },
]

const USE_MOCK_DATA = true

export default function DoctorsListPage() {
  const { id: hospitalId } = useParams()
  const navigate = useNavigate()
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [showModal, setShowModal] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [hospitalName, setHospitalName] = useState("City General Hospital")
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    specialization: "",
  })

  // Fetch doctors
  useEffect(() => {
    const fetchDoctors = async () => {
      if (USE_MOCK_DATA) {
        // Simulate API delay
        setTimeout(() => {
          setDoctors(MOCK_DOCTORS)
          setIsLoading(false)
        }, 800)
        return
      }

      // Real API call - uncomment and use this in production
      try {
        const token = localStorage.getItem("token")
        const res = await fetch(`http://localhost:8000/hospitals/${hospitalId}/doctors`, {
          headers: { Authorization: `Bearer ${token}` },
        })

        if (!res.ok) {
          throw new Error("Failed to fetch doctors")
        }

        const data = await res.json()
        setDoctors(data || [])
        setHospitalName(`Hospital ${hospitalId}`)
      } catch (err) {
        console.error(err)
        setDoctors([])
      } finally {
        setIsLoading(false)
      }
    }

    fetchDoctors()
  }, [hospitalId])

  const handleBack = () => {
    // Navigate back to superadmin hospitals dashboard
    navigate('/dashboard/superadmin')
  }

  // Form input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  // Create doctor
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSubmitting(true)

    if (USE_MOCK_DATA) {
      setTimeout(() => {
        const newDoctor = {
          id: doctors.length + 1,
          ...formData,
          image: "/doctor-placeholder.svg",
        }
        setDoctors([...doctors, newDoctor])
        setFormData({ name: "", email: "", phone: "", specialization: "" })
        setShowModal(false)
        setIsSubmitting(false)
      }, 1000)
      return
    }

    // Real API call - uncomment and use this in production
    const token = localStorage.getItem("token")

    try {
      const res = await fetch(`http://localhost:8000/hospitals/${hospitalId}/doctors`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      })

      const data = await res.json()
      if (res.ok) {
        setDoctors([
          ...doctors,
          {
            id: data.doctor_id,
            ...formData,
            image: "/doctor-placeholder.svg",
          },
        ])
        setFormData({ name: "", email: "", phone: "", specialization: "" })
        setShowModal(false)
      } else {
        alert(data.detail || data.msg || "Error creating doctor")
      }
    } catch (err) {
      console.error(err)
      alert("Error creating doctor")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={handleBack}
            className="mb-4 inline-flex items-center gap-2 text-sm font-medium text-slate-600 transition-colors hover:text-slate-900"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Hospitals
          </button>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-slate-900">{hospitalName}</h1>
              <p className="mt-2 text-sm text-slate-600">Manage doctors and medical staff</p>
            </div>
            <button
              onClick={() => setShowModal(true)}
              className="inline-flex items-center gap-2 rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition-all hover:bg-slate-800 hover:shadow-lg active:scale-95"
            >
              <Plus className="h-4 w-4" />
              Add Doctor
            </button>
          </div>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="flex min-h-[400px] items-center justify-center">
            <div className="text-center">
              <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-slate-900" />
              <p className="mt-4 text-sm text-slate-600">Loading doctors...</p>
            </div>
          </div>
        ) : doctors.length === 0 ? (
          <div className="rounded-xl border-2 border-dashed border-slate-300 bg-white">
            <div className="flex min-h-[400px] flex-col items-center justify-center py-12">
              <div className="rounded-full bg-slate-100 p-4">
                <Stethoscope className="h-8 w-8 text-slate-600" />
              </div>
              <h3 className="mt-4 text-lg font-semibold text-slate-900">No doctors yet</h3>
              <p className="mt-2 text-center text-sm text-slate-600">Get started by adding your first doctor</p>
              <button
                onClick={() => setShowModal(true)}
                className="mt-6 inline-flex items-center gap-2 rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition-all hover:bg-slate-800 hover:shadow-lg active:scale-95"
              >
                <Plus className="h-4 w-4" />
                Add Doctor
              </button>
            </div>
          </div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {doctors.map((doctor) => (
              <div
                key={doctor.id}
                className="group overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-xl"
              >
                <div className="relative aspect-square overflow-hidden bg-slate-100">
                  <img
                    src={doctor.image || "/doctor-placeholder.svg"}
                    alt={doctor.name}
                    className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
                </div>
                <div className="p-6">
                  <div className="mb-3">
                    <h3 className="text-lg font-semibold text-slate-900">{doctor.name}</h3>
                    <p className="mt-1 text-sm font-medium text-slate-600">{doctor.specialization}</p>
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <Mail className="h-4 w-4 flex-shrink-0" />
                      <span className="truncate">{doctor.email}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <Phone className="h-4 w-4 flex-shrink-0" />
                      <span>{doctor.phone}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setShowModal(false)} />

          {/* Modal */}
          <div className="relative z-10 w-full max-w-lg rounded-xl bg-white p-6 shadow-2xl">
            {/* Header */}
            <div className="mb-6 flex items-start justify-between">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Add New Doctor</h2>
                <p className="mt-1 text-sm text-slate-600">
                  Add a new doctor to {hospitalName}. Fill in all required information.
                </p>
              </div>
              <button
                onClick={() => setShowModal(false)}
                className="rounded-lg p-1 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-900"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="name" className="block text-sm font-medium text-slate-900">
                  Doctor Name
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  placeholder="Dr. John Smith"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900/10"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="specialization" className="block text-sm font-medium text-slate-900">
                  Specialization
                </label>
                <input
                  id="specialization"
                  name="specialization"
                  type="text"
                  placeholder="Cardiology, Neurology, etc."
                  value={formData.specialization}
                  onChange={handleChange}
                  required
                  className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900/10"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="email" className="block text-sm font-medium text-slate-900">
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="doctor@hospital.com"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900/10"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="phone" className="block text-sm font-medium text-slate-900">
                  Phone Number
                </label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  placeholder="+1 (555) 123-4567"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                  className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900/10"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  disabled={isSubmitting}
                  className="flex-1 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-900 transition-all hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white transition-all hover:bg-slate-800 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isSubmitting ? (
                    <span className="flex items-center justify-center gap-2">
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                      Adding...
                    </span>
                  ) : (
                    "Add Doctor"
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
