import { Button } from 'react-bootstrap';
import { PantryIngredient, pantryIngredients} from '../data/pantry';
import { PantryIngredientCard } from '../components/PantryIngredientCard';
import styles from '../styles/Pantry.module.css';


export function Pantry() {
    return (
        <>
            <div className="page_title mt-3">Pantry</div>
            <div className="d-flex justify-content-center mt-2 mb-5">
                <Button className={`${styles.custom_button}`}>Add new item</Button>
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_card_container}`}>
                    {pantryIngredients.map((ingredient: PantryIngredient) => (
                        <PantryIngredientCard key={ingredient.id} ingredient={ingredient} />
                    ))}
                </div>
            </div>
        </>
    )
}
