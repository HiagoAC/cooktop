import { Routes, Route } from 'react-router-dom';
import { AuthProvider  } from './context/AuthContext';
import { About } from './pages/About';
import { LandingPage } from './pages/LandingPage';
import { Account } from './pages/Account';
import { MealPlan } from './pages/MealPlan';
import { Recipes } from './pages/Recipes';
import { RecipeDetail } from './pages/RecipeDetail';
import { RecipeEdit } from './pages/RecipeEdit';
import { RecipeAdd } from './pages/RecipeAdd';
import { RecipeSearch } from './pages/RecipeSearch';
import { ShoppingList } from './pages/ShoppingList';
import { Pantry } from './pages/Pantry';
import { PrivateRoute } from './routes/PrivateRoute';
import { Navbar } from './components/Navbar';
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
    <AuthProvider>
      <Navbar />
      <div className={`${styles.main_container}`}>
        <Routes>
          <Route path='/' element={<LandingPage />} />
          <Route path='/meal-plan' element={<PrivateRoute />}>
            <Route path='/meal-plan' element={<MealPlan />} />
          </Route> 
          <Route path='/recipes/*' element={<PrivateRoute />}>
            <Route path='/recipes/*' element={<RecipeRoutes />} />
          </Route>
          <Route path='/shopping-list' element={<PrivateRoute />}>
            <Route path='/shopping-list' element={<ShoppingList />} />
          </Route>
          <Route path='/pantry' element={<PrivateRoute />}>
            <Route path='/pantry' element={<Pantry />} />
          </Route>
          <Route path='/account' element={<PrivateRoute />}>
            <Route path='/account' element={<Account />} />
          </Route>
          <Route path='/about' element={<About />} />
        </Routes>
      </div>
    </AuthProvider>
  )
}

export default App
