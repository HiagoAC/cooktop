import { Routes, Route } from 'react-router-dom'
import { Container } from 'react-bootstrap'
import { MealPlan } from './pages/MealPlan'
import { Recipes } from './pages/Recipes'
import { ShoppingList } from './pages/ShoppingList'
import { Pantry } from './pages/Pantry'
import { Me } from './pages/Me'
import { About } from './pages/About'


function App() {
  return <Container>
    <Routes>
      <Route path='/' element={<MealPlan />} />
      <Route path='/recipes' element={<Recipes />} />
      <Route path='/shopping-list' element={<ShoppingList />} />
      <Route path='/pantry' element={<Pantry />} />
      <Route path='/me' element={<Me />} />
      <Route path='/about' element={<About />} />
    </Routes>
  </Container>
}

export default App
