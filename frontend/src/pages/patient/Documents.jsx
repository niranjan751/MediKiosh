import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, FileText, UploadCloud, Plus, Trash2, Loader } from 'lucide-react'
import documentService from '../../services/documentService'

export default function Documents() {
  const navigate      = useNavigate()
  const fileInputRef  = useRef(null)
  const [docs,        setDocs]        = useState([])
  const [uploading,   setUploading]   = useState(false)
  const [loadingDocs, setLoadingDocs] = useState(true)
  const [error,       setError]       = useState('')

  // Load documents on mount
  useEffect(() => {
    documentService.getDocuments()
      .then(res => setDocs(res.data || []))
      .catch(() => setError('Could not load documents.'))
      .finally(() => setLoadingDocs(false))
  }, [])

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setError('')
    try {
      const uploaded = await documentService.uploadDocument(file)
      setDocs(prev => [uploaded, ...prev])
    } catch (err) {
      setError(err.response?.data?.message || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
      // Reset input so same file can be re-selected
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this document?')) return
    try {
      await documentService.deleteDocument(id)
      setDocs(prev => prev.filter(d => d._id !== id))
    } catch {
      alert('Could not delete. Please try again.')
    }
  }

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/patient/interview')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>Medical Documents</h1>
        <button onClick={() => navigate('/patient/timeline')} style={{ padding: '8px 16px', background: '#00897b', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
          Continue to Timeline <ArrowRight size={16} style={{ display: 'inline', verticalAlign: 'text-bottom' }}/>
        </button>
      </header>

      <div style={{ flex: 1, padding: '40px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>

        {/* Upload drop zone */}
        <div
          onClick={() => !uploading && fileInputRef.current?.click()}
          style={{ backgroundColor: 'white', padding: '40px', borderRadius: '16px', border: '2px dashed #cbd5e1', textAlign: 'center', marginBottom: '32px', cursor: uploading ? 'not-allowed' : 'pointer', opacity: uploading ? 0.7 : 1 }}
        >
          {uploading
            ? <Loader size={48} color="#1565c0" style={{ marginBottom: '16px', animation: 'spin 1s linear infinite' }} />
            : <UploadCloud size={48} color="#1565c0" style={{ marginBottom: '16px' }} />
          }
          <h2 style={{ fontSize: '20px', color: '#1e293b', margin: '0 0 8px 0' }}>
            {uploading ? 'Uploading…' : 'Upload Prescriptions or Reports'}
          </h2>
          <p style={{ color: '#64748b', margin: '0 0 24px 0' }}>
            {uploading ? 'Please wait while your file is being uploaded.' : 'Tap here to take a photo or upload a file (PDF, JPG, PNG).'}
          </p>
          {!uploading && (
            <button style={{ padding: '12px 24px', backgroundColor: '#f0f7ff', color: '#1565c0', border: '1px solid #1565c0', borderRadius: '8px', fontWeight: '600', cursor: 'pointer' }}>
              <Plus size={16} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '8px' }}/>Select File
            </button>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.jpg,.jpeg,.png,.tiff,.bmp"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>

        {error && (
          <p style={{ color: '#ef4444', marginBottom: '16px', textAlign: 'center' }}>{error}</p>
        )}

        <h3 style={{ fontSize: '18px', color: '#1e293b', marginBottom: '16px' }}>
          Uploaded Documents {docs.length > 0 && `(${docs.length})`}
        </h3>

        {loadingDocs && (
          <p style={{ color: '#64748b', textAlign: 'center' }}>Loading documents…</p>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {docs.map((doc) => (
            <div key={doc._id} style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <div style={{ width: '48px', height: '48px', backgroundColor: '#e0f2fe', color: '#0284c7', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <FileText size={24} />
                </div>
                <div>
                  <h4 style={{ margin: '0 0 4px 0', fontSize: '16px', color: '#1e293b' }}>{doc.originalName}</h4>
                  <p style={{ margin: 0, fontSize: '13px', color: '#64748b' }}>
                    {new Date(doc.createdAt).toLocaleDateString()} • OCR: {doc.ocrStatus || 'pending'}
                    {doc.fileSize && ` • ${(doc.fileSize / 1024).toFixed(1)} KB`}
                  </p>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  onClick={() => navigate('/patient/ocr', { state: { docId: doc._id } })}
                  style={{ padding: '8px 16px', backgroundColor: 'transparent', color: '#1565c0', border: '1px solid #1565c0', borderRadius: '6px', fontWeight: '600', cursor: 'pointer' }}
                >
                  View OCR
                </button>
                <button
                  onClick={() => handleDelete(doc._id)}
                  style={{ padding: '8px', backgroundColor: 'transparent', color: '#ef4444', border: '1px solid #fecaca', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
                  title="Delete document"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}

          {!loadingDocs && docs.length === 0 && (
            <p style={{ textAlign: 'center', color: '#94a3b8', marginTop: '16px' }}>
              No documents uploaded yet. Upload a prescription or lab report above.
            </p>
          )}
        </div>
      </div>
    </main>
  )
}
