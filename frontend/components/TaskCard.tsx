import React, { useState } from 'react';
import { Task } from '../types';
import Button from './ui/Button';
import Link from 'next/link';

interface TaskCardProps {
  task: Task;
  onToggleComplete?: (id: string) => void;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggleComplete, onEdit, onDelete }) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const handleDelete = () => {
    if (onDelete) {
      setIsDeleting(true);
      onDelete(task.id);
    }
  };

  const handleToggleComplete = () => {
    if (onToggleComplete) {
      onToggleComplete(task.id);
    }
  };

  return (
    <div
      className={`bg-white rounded-2xl p-6 mb-4 card-elevated transition-all duration-300 ${
        task.completed ? 'bg-green-50 border-l-4 border-green-500' : 'bg-white border-l-4 border-blue-500'
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          className={`h-6 w-6 rounded-full border-2 cursor-pointer transition-all duration-300 ${
            task.completed
              ? 'bg-green-500 border-green-500 checked:bg-green-500'
              : 'bg-white border-gray-300 hover:border-blue-500'
          }`}
        />
        <div className="ml-4 flex-1">
          <h3 className={`text-lg font-bold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-2 ${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
          <div className="mt-3 flex flex-wrap items-center text-sm">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              task.completed ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
            }`}>
              {task.completed ? 'Completed' : 'Pending'}
            </span>
            <span className="ml-2 text-gray-500">
              Created: {new Date(task.createdAt).toLocaleDateString()}
            </span>
            {task.updatedAt && task.updatedAt !== task.createdAt && (
              <span className="ml-2 text-gray-500">
                Updated: {new Date(task.updatedAt).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>
        <div className={`flex space-x-2 transition-opacity duration-300 ${isHovered ? 'opacity-100' : 'opacity-0'}`}>
          <Link href={`/tasks/edit/${task.id}`}>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => onEdit && onEdit(task.id)}
              className="shadow-sm hover:shadow-md"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Edit
            </Button>
          </Link>
          <Button
            variant="danger"
            size="sm"
            onClick={handleDelete}
            isLoading={isDeleting}
            className="shadow-sm hover:shadow-md"
          >
            {isDeleting ? (
              <>
                <svg className="animate-spin -ml-1 mr-1 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Deleting...
              </>
            ) : (
              <>
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Delete
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;