import { Container } from 'react-bootstrap';
import { FormCard } from '../components/FormCard';
import { RecipeForm } from '../components/RecipeForm';


export function RecipeAdd() {
    return (
        <Container className="pb-4">
            <FormCard
                title="Add a New Recipe"
                formComponent={< RecipeForm/>}
                buttonText="Add Recipe"
            />
        </Container>
    )
}
