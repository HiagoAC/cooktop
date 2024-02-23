import { Routes, Route } from 'react-router-dom'
import { Container } from 'react-bootstrap'
import { MealPlan } from './pages/MealPlan'
import { Recipes } from './pages/Recipes'
import { RecipeDetail } from './pages/RecipeDetail'
import { RecipeEdit } from './pages/RecipeEdit'
import { RecipeAdd } from './pages/RecipeAdd'
import { RecipeSearch } from './pages/RecipeSearch'
import { ShoppingList } from './pages/ShoppingList'
import { Pantry } from './pages/Pantry'
import { Me } from './pages/Me'
import { About } from './pages/About'
import { Navbar } from './components/Navbar'
import styles from './styles/App.module.css';
import './styles/global.css';


function RecipeRoutes() {
  return (
    <Routes>
      <Route path='/' element={<Recipes />} />
      <Route path='/add' element={<RecipeAdd />} />
      <Route path='/search' element={<RecipeSearch />} />
      <Route path='/:id' element={<RecipeDetail />} />
      <Route path='/:id/edit' element={<RecipeEdit />} />
    </Routes>
  );
}


function App() {
  return (
    <>
      <Navbar />
      <Container className={`pb-4 ${styles.main_container}`}>
        <Routes>
          <Route path='/' element={<MealPlan />} /> 
          <Route path='/recipes/*' element={<RecipeRoutes />} />
          <Route path='/shopping-list' element={<ShoppingList />} />
          <Route path='/pantry' element={<Pantry />} />
          <Route path='/me' element={<Me />} />
          <Route path='/about' element={<About />} />
        </Routes>
      </Container>
    </>
  )
}

export default App
