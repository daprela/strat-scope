import { createRoot } from 'react-dom/client';
import { Foundation } from './Foundation';
import './tokens.css';

const root = document.getElementById('root');
if (!root) throw new Error('Missing local entry');
createRoot(root).render(<Foundation />);
