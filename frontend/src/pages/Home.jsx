import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Home = () => {
    return (
        <div className="space-y-12">
            <section className="text-center py-20 bg-gradient-to-r from-primary-600 to-primary-800 rounded-3xl text-white px-4">
                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6"
                >
                    Quality Steel for Every Construction
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="text-xl md:text-2xl text-primary-100 max-w-3xl mx-auto mb-10"
                >
                    Premium TMT bars, sheets, pipes, and structural steel at wholesale prices.
                </motion.p>
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <Link to="/products" className="inline-block bg-white text-primary-700 font-bold py-3 px-8 rounded-full text-lg shadow-lg hover:bg-gray-100 transition-colors">
                        Shop Now
                    </Link>
                </motion.div>
            </section>

            <section>
                <h2 className="text-3xl font-bold text-gray-900 mb-8">Featured Categories</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {['Construction Steel', 'Sheets & Plates', 'Pipes & Tubes'].map((cat, idx) => (
                        <Link key={idx} to={`/products?category=${cat.toLowerCase().replace(/ & /g, '-').replace(/ /g, '-')}`} className="group relative rounded-xl overflow-hidden shadow-lg aspect-video">
                            <div className="absolute inset-0 bg-gray-900/40 group-hover:bg-gray-900/30 transition-colors z-10" />
                            <img src={`https://placehold.co/600x400?text=${cat}`} alt={cat} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                            <div className="absolute inset-0 flex items-center justify-center z-20">
                                <h3 className="text-2xl font-bold text-white">{cat}</h3>
                            </div>
                        </Link>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default Home;
