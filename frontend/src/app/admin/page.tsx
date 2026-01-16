'use client';

import { useState, useRef, useEffect } from 'react';
import { Upload, FileText, X } from 'lucide-react';

export default function AdminPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [knowledgeDocs, setKnowledgeDocs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus(null);
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setUploadStatus(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      // Use the correct API endpoint for admin upload
      const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendBaseUrl}/api/admin/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_ADMIN_TOKEN || 'secret_key_for_ai_brain_by_@umarprogrammer19!#'}`,
        },
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setUploadStatus(`Success: Document uploaded successfully`);
        // Refresh the knowledge docs list
        fetchKnowledgeDocs();
        // Reset selected file
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      } else {
        setUploadStatus(`Error: ${result.detail || 'Upload failed'}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Error: Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  // Fetch knowledge documents
  const fetchKnowledgeDocs = async () => {
    try {
      const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendBaseUrl}/api/admin/documents`, {
        headers: {
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_ADMIN_TOKEN || 'secret_key_for_ai_brain_by_@umarprogrammer19!#'}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setKnowledgeDocs(data || []);
      } else {
        console.error('Failed to fetch documents');
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  // Load knowledge docs on component mount
  useEffect(() => {
    fetchKnowledgeDocs();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage ketamine therapy knowledge base</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload Section */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload Document</h2>

            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-600">
                  {selectedFile ? selectedFile.name : 'Click to select a file or drag and drop'}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  PDF, DOCX, TXT, or MD files (max 10MB)
                </p>

                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept=".pdf,.docx,.txt,.md"
                  className="hidden"
                />

                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                >
                  Select File
                </button>
              </div>

              {selectedFile && (
                <div className="flex items-center justify-between bg-gray-50 p-3 rounded">
                  <div className="flex items-center">
                    <FileText className="h-5 w-5 text-blue-500 mr-2" />
                    <span className="text-sm font-medium truncate max-w-xs">{selectedFile.name}</span>
                    <span className="text-xs text-gray-500 ml-2">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                  <button
                    onClick={() => {
                      setSelectedFile(null);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = '';
                      }
                    }}
                    className="text-red-500 hover:text-red-700"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
              )}

              <button
                onClick={handleUpload}
                disabled={!selectedFile || loading}
                className={`w-full py-3 px-4 rounded-md text-white font-medium ${
                  !selectedFile || loading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700'
                }`}
              >
                {loading ? 'Uploading...' : 'Upload Document'}
              </button>

              {uploadStatus && (
                <div
                  className={`p-3 rounded-md text-sm ${
                    uploadStatus.startsWith('Success')
                      ? 'bg-green-50 text-green-800'
                      : 'bg-red-50 text-red-800'
                  }`}
                >
                  {uploadStatus}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Knowledge Table */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Knowledge Base</h2>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Filename
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Uploaded
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {knowledgeDocs.length > 0 ? (
                    knowledgeDocs.map((doc) => (
                      <tr key={doc.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {doc.filename || doc.fileName}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span
                            className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              doc.isKetamineRelevant || doc.relevant
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {doc.isKetamineRelevant || doc.relevant ? 'Active Training' : 'Rejected'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(doc.uploadDate || doc.created_at || doc.upload_date).toLocaleDateString()}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={3} className="px-6 py-4 text-center text-sm text-gray-500">
                        No documents uploaded yet
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}