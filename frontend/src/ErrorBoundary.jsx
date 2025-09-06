// frontend/src/ErrorBoundary.jsx
import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true, error: error };
    }

    componentDidCatch(error, errorInfo) {
        // You can also log the error to an error reporting service here
        console.error("Uncaught error:", error, errorInfo);
        this.setState({ errorInfo: errorInfo });
    }

    render() {
        if (this.state.hasError) {
            // You can render any custom fallback UI
            // For debugging, we will render the actual error message.
            return (
                <div style={{ padding: '20px', backgroundColor: '#fff0f0', border: '1px solid #ffaaaa', borderRadius: '8px', color: '#d8000c' }}>
                    <h1>Something went wrong.</h1>
                    <p>This is the error that is causing the blank screen:</p>
                    <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
            {this.state.error && this.state.error.toString()}
          </pre>
                    <h3>Component Stack:</h3>
                    <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </pre>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;