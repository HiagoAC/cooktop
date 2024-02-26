import { Container } from 'react-bootstrap';
import { FormCard } from '../components/FormCard';
import { SearchForm } from '../components/SearchForm';


export function RecipeSearch() {
    return (
        <Container className="pb-4">
            <FormCard
                title="Search for Recipes"
                formComponent={<SearchForm />}
                buttonText="Search"
            />
        </Container>
    )
}
