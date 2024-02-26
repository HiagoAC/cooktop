import { useLocation } from 'react-router-dom';
import { FormCard } from '../components/FormCard';
import { RecipeForm } from '../components/RecipeForm';
import { Recipe } from '../data/recipe_detail';
import { Container } from 'react-bootstrap';


export function RecipeEdit() {
    const location = useLocation();
    const recipe: Recipe = location.state.recipe;

    return (
        <Container className="pb-4">
            <FormCard
                title="Edit Recipe"
                formComponent={<RecipeForm recipe={recipe} withUrlField={false} />}
                buttonText="Save"
            />
        </Container>
    )
}
