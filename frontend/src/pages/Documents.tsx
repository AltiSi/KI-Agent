import { useEffect, useState } from 'react';
import { documentsApi } from '../services/api';
import type { Document } from '../types';
import { format } from 'date-fns';
import { de } from 'date-fns/locale';
import { Upload, FileText, Trash2, Eye } from 'lucide-react';

export default function Documents() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const data = await documentsApi.getAll();
      setDocuments(data);
    } catch (error) {
      console.error('Fehler beim Laden der Dokumente:', error);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await documentsApi.upload(file);
      await loadDocuments();
      alert('Dokument erfolgreich hochgeladen und analysiert! ✅');
    } catch (error) {
      console.error('Fehler beim Upload:', error);
      alert('Fehler beim Hochladen des Dokuments');
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Dokument wirklich löschen?')) return;

    try {
      await documentsApi.delete(id);
      setDocuments(documents.filter((d) => d.id !== id));
      if (selectedDocument?.id === id) {
        setSelectedDocument(null);
      }
    } catch (error) {
      console.error('Fehler beim Löschen:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dokumente</h1>

        <label className="btn btn-primary cursor-pointer">
          <Upload className="w-4 h-4 mr-2 inline" />
          {uploading ? 'Wird hochgeladen...' : 'Dokument hochladen'}
          <input
            type="file"
            className="hidden"
            accept=".pdf,.docx,.txt,.jpg,.jpeg,.png"
            onChange={handleFileUpload}
            disabled={uploading}
          />
        </label>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Dokumentenliste */}
        <div className="space-y-3">
          {documents.length === 0 ? (
            <div className="card text-center py-12 text-gray-500">
              <FileText className="w-12 h-12 mx-auto mb-3 text-gray-400" />
              <p>Noch keine Dokumente hochgeladen</p>
              <p className="text-sm mt-1">
                Lade dein erstes Dokument hoch und ich analysiere es für dich!
              </p>
            </div>
          ) : (
            documents.map((doc) => (
              <div
                key={doc.id}
                className={`card cursor-pointer transition-all ${
                  selectedDocument?.id === doc.id
                    ? 'ring-2 ring-primary-500'
                    : 'hover:shadow-lg'
                }`}
                onClick={() => setSelectedDocument(doc)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3 flex-1">
                    <FileText className="w-5 h-5 text-gray-400 mt-1" />
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 truncate">
                        {doc.title}
                      </h3>
                      {doc.category && (
                        <span className="inline-block mt-1 px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded">
                          {doc.category}
                        </span>
                      )}
                      <p className="text-sm text-gray-500 mt-1">
                        {format(new Date(doc.created_at), 'dd. MMM yyyy', {
                          locale: de,
                        })}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(doc.id);
                    }}
                    className="text-gray-400 hover:text-red-600 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Dokumentendetails */}
        <div className="lg:sticky lg:top-8">
          {selectedDocument ? (
            <div className="card">
              <h2 className="text-xl font-bold mb-4 flex items-center">
                <Eye className="w-5 h-5 mr-2" />
                Analyse: {selectedDocument.title}
              </h2>

              <div className="space-y-4">
                {/* Zusammenfassung */}
                {selectedDocument.summary && (
                  <div>
                    <h3 className="font-semibold text-gray-700 mb-2">
                      📝 Zusammenfassung
                    </h3>
                    <p className="text-gray-600 bg-gray-50 p-3 rounded-lg">
                      {selectedDocument.summary}
                    </p>
                  </div>
                )}

                {/* Wichtige Informationen */}
                {selectedDocument.important_info && (
                  <div>
                    <h3 className="font-semibold text-gray-700 mb-2">
                      ⭐ Wichtige Informationen
                    </h3>
                    <p className="text-gray-600 bg-yellow-50 p-3 rounded-lg">
                      {selectedDocument.important_info}
                    </p>
                  </div>
                )}

                {/* Nächste Schritte */}
                {selectedDocument.next_steps && (
                  <div>
                    <h3 className="font-semibold text-gray-700 mb-2">
                      ✅ Nächste Schritte
                    </h3>
                    <div className="bg-green-50 p-3 rounded-lg">
                      {selectedDocument.next_steps.split('\n').map((step, i) => (
                        <p key={i} className="text-gray-600">
                          {step}
                        </p>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="card text-center py-12 text-gray-500">
              <Eye className="w-12 h-12 mx-auto mb-3 text-gray-400" />
              <p>Wähle ein Dokument aus, um die Analyse zu sehen</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
