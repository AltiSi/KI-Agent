import { useEffect, useState } from 'react';
import { shoppingApi } from '../services/api';
import type { ShoppingList } from '../types';
import { ShoppingCart, Plus, Trash2 } from 'lucide-react';

export default function Shopping() {
  const [lists, setLists] = useState<ShoppingList[]>([]);
  const [selectedList, setSelectedList] = useState<ShoppingList | null>(null);
  const [newItemText, setNewItemText] = useState('');

  useEffect(() => {
    loadLists();
  }, []);

  const loadLists = async () => {
    try {
      const data = await shoppingApi.getLists();
      setLists(data);
      if (data.length > 0 && !selectedList) {
        setSelectedList(data[0]);
      }
    } catch (error) {
      console.error('Fehler beim Laden:', error);
    }
  };

  const createList = async () => {
    const name = prompt('Name der neuen Einkaufsliste:');
    if (!name) return;

    try {
      const list = await shoppingApi.createList(name);
      setLists([...lists, list]);
      setSelectedList(list);
    } catch (error) {
      console.error('Fehler beim Erstellen:', error);
    }
  };

  const addItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedList || !newItemText.trim()) return;

    try {
      await shoppingApi.addItem(selectedList.id, { item: newItemText });
      setNewItemText('');
      const updated = await shoppingApi.getList(selectedList.id);
      setSelectedList(updated);
      setLists(lists.map((l) => (l.id === updated.id ? updated : l)));
    } catch (error) {
      console.error('Fehler beim Hinzufügen:', error);
    }
  };

  const toggleItem = async (itemId: number, checked: boolean) => {
    if (!selectedList) return;

    try {
      await shoppingApi.toggleItem(itemId, !checked);
      const updated = await shoppingApi.getList(selectedList.id);
      setSelectedList(updated);
      setLists(lists.map((l) => (l.id === updated.id ? updated : l)));
    } catch (error) {
      console.error('Fehler:', error);
    }
  };

  const deleteItem = async (itemId: number) => {
    if (!selectedList) return;

    try {
      await shoppingApi.deleteItem(itemId);
      const updated = await shoppingApi.getList(selectedList.id);
      setSelectedList(updated);
      setLists(lists.map((l) => (l.id === updated.id ? updated : l)));
    } catch (error) {
      console.error('Fehler:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Einkaufslisten</h1>
        <button onClick={createList} className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2 inline" />
          Neue Liste
        </button>
      </div>

      {lists.length === 0 ? (
        <div className="card text-center py-12 text-gray-500">
          <ShoppingCart className="w-12 h-12 mx-auto mb-3 text-gray-400" />
          <p>Noch keine Einkaufslisten erstellt</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Listen-Auswahl */}
          <div className="space-y-3">
            {lists.map((list) => (
              <div
                key={list.id}
                onClick={() => setSelectedList(list)}
                className={`card cursor-pointer transition-all ${
                  selectedList?.id === list.id
                    ? 'ring-2 ring-primary-500'
                    : 'hover:shadow-lg'
                }`}
              >
                <h3 className="font-semibold">{list.name}</h3>
                <p className="text-sm text-gray-600 mt-1">
                  {list.items.length} Items
                </p>
              </div>
            ))}
          </div>

          {/* Ausgewählte Liste */}
          {selectedList && (
            <div className="lg:col-span-2 card">
              <h2 className="text-xl font-bold mb-4">{selectedList.name}</h2>

              {/* Neues Item hinzufügen */}
              <form onSubmit={addItem} className="mb-4">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    className="input flex-1"
                    placeholder="Neues Item hinzufügen..."
                    value={newItemText}
                    onChange={(e) => setNewItemText(e.target.value)}
                  />
                  <button type="submit" className="btn btn-primary">
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
              </form>

              {/* Items */}
              <div className="space-y-2">
                {selectedList.items.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">
                    Liste ist leer
                  </p>
                ) : (
                  selectedList.items.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center space-x-3 flex-1">
                        <input
                          type="checkbox"
                          checked={item.checked}
                          onChange={() => toggleItem(item.id, item.checked)}
                          className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500"
                        />
                        <span
                          className={
                            item.checked
                              ? 'line-through text-gray-500'
                              : 'text-gray-900'
                          }
                        >
                          {item.item}
                        </span>
                      </div>
                      <button
                        onClick={() => deleteItem(item.id)}
                        className="text-gray-400 hover:text-red-600 transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
